#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import time


class RestartSelfIfUpdated:
    """检测脚本自身更新并重启"""

    mtime = 0

    def __init__(self, file=__file__):
        mtime = os.path.getmtime(file)
        time_format = '%H:%M'
        if self.mtime and mtime != self.mtime:
            print(
                file,
                'mtime changed:',
                time.strftime(time_format, time.localtime(self.mtime)),
                'to',
                time.strftime(time_format, time.localtime(mtime)),
                ', restarting...',
            )
            self.restart()
        RestartSelfIfUpdated.mtime = os.path.getmtime(file)

    def restart(self):
        python = sys.executable
        os.execl(python, python, *sys.argv)
