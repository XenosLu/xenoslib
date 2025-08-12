#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import logging

import yaml

from xenoslib.base import SingletonWithArgs


logger = logging.getLogger(__name__)


class ConfigLoader(SingletonWithArgs):
    """Centralized configuration management with optional Vault integration.

    Args:
        config_file_path (str): Path to the YAML configuration file. Defaults to "config.yml".
        vault_secret_id (str, optional): Secret ID for Vault authentication.
            If provided, enables Vault functionality and imports hvac module.

    Attributes:
        cache (dict): Cache storage for frequently accessed configuration values.

    Example:
        # Without Vault (hvac not imported)
        >>> config = ConfigLoader("config.yml")

        # With Vault (hvac imported on demand)
        >>> config = ConfigLoader("config.yml", vault_secret_id="my-secret-id")
    """

    # 常量定义优化
    VAULT_SUFFIX = "@vault"
    KV_MOUNT_POINT = "kv"
    
    cache = {}
    vault_client = None

    def __init__(self, config_file_path="config.yml", vault_secret_id=None):
        """Initialize the ConfigLoader with a configuration file and optional Vault secret."""
        with open(config_file_path, "r") as f:
            # 增强空文件处理
            config_data = yaml.safe_load(f)
            self._raw_config = config_data if isinstance(config_data, dict) else {}
        
        if vault_secret_id is not None:
            self.vault_secret_id = vault_secret_id
            self._check_and_renew_vault_client()

    def _init_vault_client(self):
        """Initialize and authenticate the Vault client (imports hvac on demand).

        Args:
            vault_secret_id (str): Secret ID for Vault authentication.

        Raises:
            ImportError: If hvac package is not installed.
            KeyError: If required Vault configuration is missing.
            Exception: If Vault authentication fails.
        """
        try:
            import hvac  # Lazy import
        except ImportError as e:
            raise ImportError(
                "hvac package is required for Vault integration. Install with: pip install hvac"
            ) from e

        try:
            vault_config = self._raw_config.get("vault", {})
            vault_url = vault_config.get("url")
            vault_space = vault_config.get("space")
            vault_role_id = vault_config.get("role_id")

            if not all([vault_url, vault_space, vault_role_id]):
                raise KeyError("Missing required Vault configuration in config.yml")

            self.vault_client = hvac.Client(url=vault_url, namespace=vault_space, timeout=45)
            self.vault_client.auth.approle.login(
                role_id=vault_role_id, secret_id=self.vault_secret_id
            )
        except Exception as e:
            self.vault_client = None
            # 完善异常链
            raise Exception(f"Failed to initialize Vault client: {str(e)}") from e

    def _check_and_renew_vault_client(self):
        # 检查当前Token的状态，包括过期时间和可续租性
        if not self.vault_client or not self.vault_client.is_authenticated():
            # 如果当前Token无效，则重新认证
            self._init_vault_client()

    def _is_vault_reference(self, section_config, key_name):
        """检查键是否是Vault引用"""
        return f"{key_name}{self.VAULT_SUFFIX}" in section_config

    def get(self, section, key_name, use_cache=True):
        """Retrieve a configuration value.

        Args:
            section (str): The configuration section name.
            key_name (str): The key name within the section.
            use_cache (bool): Whether to use cached values. Defaults to True.

        Returns:
            The configuration value, which may come from:
            - Direct configuration value
            - Vault secret (if Vault is initialized)
            - Cache (if enabled)

        Raises:
            KeyError: If the section or key is not found.
            Exception: If Vault access is required but not available.
        """
        section_config = self._raw_config.get(section)
        if section_config is None:
            raise KeyError(f"Section '{section}' not found")

        # Check for direct value first
        if key_name in section_config:
            return section_config[key_name]

        # Handle Vault reference if Vault is enabled
        if self._is_vault_reference(section_config, key_name):
            if self.vault_client is None:
                raise Exception(
                    f"Vault access required for {key_name} but Vault is not initialized"
                )

            # 使用标准分隔符的缓存键
            cache_key = f"{section}:{key_name}"

            if use_cache and cache_key in self.cache:
                return self.cache[cache_key]
            value = self._get_value_from_vault(section, key_name)
            self.cache[cache_key] = value
            return value

        raise KeyError(f"Key '{key_name}' not found in section '{section}'")

    def _get_value_from_vault(self, section, key_name):
        """Retrieve a secret value from Vault.

        Args:
            section (str): The configuration section name.
            key_name (str): The key name within the section.

        Returns:
            The secret value from Vault.

        Raises:
            Exception: If Vault access fails.
        """
        try:
            section_config = self._raw_config[section]
            vault_path = section_config.get("vault_path")
            if not vault_path:
                raise KeyError(f"Missing vault_path in section '{section}'")

            vault_key_ref = f"{key_name}{self.VAULT_SUFFIX}"
            vault_key = section_config[vault_key_ref]
            
            # 简化命名空间处理逻辑
            namespace = section_config.get("vault_namespace") or self._raw_config["vault"]["space"]
            self.vault_client.adapter.namespace = namespace
            
            data = self.vault_client.secrets.kv.read_secret_version(
                path=vault_path, mount_point=self.KV_MOUNT_POINT, raise_on_deleted_version=True
            )
            return data["data"]["data"][vault_key]
        except Exception as e:
            # 完善异常链
            raise Exception(f"Failed to fetch {key_name} from Vault: {str(e)}") from e

    def __getitem__(self, section):
        """Dictionary-style access to configuration sections."""
        if section not in self._raw_config:
            raise KeyError(f"Section '{section}' not found")
        return SectionProxy(self, section)

    def __getattr__(self, section):
        """Attribute-style access to configuration sections."""
        try:
            return self[section]
        except KeyError as e:
            raise AttributeError(str(e))


class SectionProxy:
    """Proxy class for configuration section access."""

    def __init__(self, config_loader, section):
        self._loader = config_loader
        self._section = section

    def __getitem__(self, key):
        """Dictionary-style access to configuration values."""
        return self._loader.get(self._section, key)

    def get(self, key, default=None):
        """Dictionary-style access to configuration values."""
        try:
            return self._loader.get(self._section, key)
        except KeyError:
            return default

    def __getattr__(self, key):
        """Attribute-style access to configuration values."""
        try:
            return self[key]
        except KeyError as e:
            raise AttributeError(str(e))

    def __repr__(self):
        """String representation of the section's configuration."""
        return yaml.dump(self._loader._raw_config[self._section])


if __name__ == "__main__":
    config_without_vault = ConfigLoader("config.yml")
    print("Without Vault:", config_without_vault.get("jira", "url"))

    # This will only work if you provide a valid Vault secret ID
    # and hvac package is installed
    config_with_vault = ConfigLoader("config.yml", vault_secret_id=os.getenv("VAULT_SECRET_ID"))

    print("With Vault:", config_with_vault.test.test)
    print("With Vault:", config_with_vault["cis"]["cis_client_id"])
    print("Try val not exists: ", config_with_vault.test.get("not_exists"))
