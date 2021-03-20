#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import time


class RestartSelfIfUpdated:
    """检测自身更新并重启"""

    mtime = 0

    def __init__(self):
        mtime = os.path.getmtime(__file__)
        if self.mtime and mtime != self.mtime:
            print(
                __file__,
                'mtime changed:',
                time.strftime('%H%M', time.localtime(self.mtime)),
                'to',
                time.strftime('%H%M', time.localtime(mtime)),
                ', restarting...',
            )
            self.restart()
        RestartSelfIfUpdated.mtime = os.path.getmtime(__file__)

    def restart(self):
        python = sys.executable
        os.execl(python, python, *sys.argv)
