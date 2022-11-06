#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import ctypes
import time
import msvcrt


class RunAsAdmin:
    """
    Usage: RunAsAdmin(main, cmd=True)
    """

    @staticmethod
    def is_admin():
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except Exception as exc:
            print(exc)
            return False

    def __init__(self, func, cmd=False):
        if self.is_admin():
            func()
            return
        elif cmd:
            self.run_as_admin_in_cmd()
        else:
            self.run_as_admin()
        print("Need administrator privilege, trying run as admin...")

    @staticmethod
    def run_as_admin():
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, " ".join(sys.argv), None, 1
        )

    @staticmethod
    def run_as_admin_in_cmd():
        arg_line = f'/k {sys.executable} "{os.path.abspath(sys.argv[0])}" {" ".join(sys.argv[1:])}'
        ctypes.windll.shell32.ShellExecuteW(None, "runas", "cmd", arg_line, None, 1)


def pause():
    print("Press any key to continue...")
    msvcrt.getch()
    while msvcrt.kbhit():
        msvcrt.getch()


def timeout(seconds):
    for second in range(seconds - 1, -1, -1):
        if msvcrt.kbhit():
            break
        print(f"Waiting {second}s , press any key to continue...", end="\r")
        time.sleep(1)
    print()  # make sure the message won't be covered
