#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import ctypes
import time
import msvcrt
import winreg


def refresh_update_env():
    """refresh after update environment"""
    HWND_BROADCAST = 0xFFFF
    WM_SETTINGCHANGE = 0x1A
    SMTO_ABORTIFHUNG = 0x0002

    result = ctypes.c_long()
    ctypes.windll.user32.SendMessageTimeoutW(
        HWND_BROADCAST,
        WM_SETTINGCHANGE,
        0,
        "Environment",
        SMTO_ABORTIFHUNG,
        5000,
        ctypes.byref(result),
    )


def add_windows_path_env(new_path):
    """Add directory to Windows path environment variable"""
    print(f"Adding directory to path: {new_path}")
    path_key = winreg.OpenKey(
        winreg.HKEY_LOCAL_MACHINE,
        r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment",
        0,
        winreg.KEY_ALL_ACCESS,
    )
    path_str, _ = winreg.QueryValueEx(path_key, "Path")
    path_list = path_str.split(";")
    if new_path in path_list:
        print(f"{new_path} already exists in the path")
        return False
    else:
        print(f"Added {new_path} to the path")
        path_list.append(new_path)
        new_path = ";".join(path_list)
        winreg.SetValueEx(path_key, "Path", 0, winreg.REG_EXPAND_SZ, new_path)
        try:
            winreg.SetValueEx(path_key, "Path", 0, winreg.REG_EXPAND_SZ, new_path)
            refresh_update_env()
            return True
        except Exception as exc:
            print(f"Failed to update the path: {str(exc)}")
            return False


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
        arg_line = (
            f'/k start "{sys.executable}" "{os.path.abspath(sys.argv[0])}" {" ".join(sys.argv[1:])}'
        )
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


def test():
    add_windows_path_env('c:\\falloutx')
    print("added")
    pause()

if __name__ == "__main__":
    RunAsAdmin(test, cmd=True)

