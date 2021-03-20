#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os

import yaml


class YamlConfig(SingletonWithArgs, dict):
    def __getattr__(self, key):
        return self.get(key)

    def __setattr__(self, name, value):
        if name.startswith('_'):
            super().__setattr__(name, value)
        else:
            self[name] = value

    def __str__(self):
        return yaml.safe_dump(self.copy(), allow_unicode=True)

    def __init__(self, config_file='config.yml'):
        if self._config_file:
            return
        self._config_file = config_file
        if os.path.exists(config_file):
            with open(config_file, encoding='utf-8') as r:
                self.update(yaml.safe_load(r))

    def save(self):
        with open(self._config_file, 'w', encoding='utf-8') as w:
            yaml.safe_dump(self.copy(), w, allow_unicode=True)
