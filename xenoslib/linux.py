#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import time
import os
import termios
import select
import tty


def pause():
    print('Press any key to continue...')
    # 获取标准输入(终端)的设置
    old_settings = termios.tcgetattr(sys.stdin)

    new_settings = old_settings[:]

    # 使用非规范模式(索引3是c_lflag 也就是本地模式)
    new_settings[3] &= ~termios.ICANON

    # 关闭回显(输入不会被显示)
    new_settings[3] &= ~termios.ECHO

    termios.tcsetattr(sys.stdin, termios.TCSANOW, new_settings)  # 使设置生效
    os.read(sys.stdin.fileno(), 7)  # 读入字符
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)  # recover terminal


def timeout(seconds):
    old_settings = termios.tcgetattr(sys.stdin)
    tty.setcbreak(sys.stdin.fileno())
    for second in range(seconds, 0, -1):
        print(f'Waiting {second}s , press any key to continue...', end='\r')
        break_flag = False
        for i in range(1000):
            time.sleep(0.001)
            if select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], []):
                sys.stdin.read(1)
                break_flag = True
                break
        if break_flag:
            break
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)  # recover terminal


if __name__ == '__main__':
    pause()
