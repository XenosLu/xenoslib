#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os

import yaml

from xenoslib.base import SingletonWithArgs


class YamlConfig(SingletonWithArgs, dict):
    """yaml格式配置管理"""
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
        data = str(self)
        with open(self._config_file, 'w', encoding='utf-8') as w:
            w.write(data)
            # yaml.safe_dump(self.copy(), w, allow_unicode=True)


def del_to_recyclebin(filepath, on_fail_delete=False):
    """删除文件到回收站"""
    if not platform.system() == 'Windows':
        if on_fail_delete:
            os.remove(filepath)
            return True
        return False
    from win32com.shell import shell, shellcon

    res, _ = shell.SHFileOperation(
        (
            0,
            shellcon.FO_DELETE,
            filepath,
            None,
            shellcon.FOF_SILENT | shellcon.FOF_ALLOWUNDO | shellcon.FOF_NOCONFIRMATION,
            None,
            None,
        )
    )
    return res == 0
