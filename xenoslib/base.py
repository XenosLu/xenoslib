#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import sys
import time


def color(value, color_name='blue'):
    """
    return text with color, default in blue.
    "Why is it blue?"
    "It's always blue."
    """
    color_code = {
        'red': 31,
        'green': 32,
        'yellow': 33,
        'blue': 34,
        'magenta': 35,
        'cyan': 36,
    }
    if sys.platform == 'win32':
        return value
    else:
        return '\033[1;{code}m{value}\033[0m'.format(code=color_code[color_name], value=value)


def pause_windows():
    import msvcrt

    msvcrt.getch()


def pause_linux():
    import os
    import termios

    # 获取标准输入的描述符
    fd = sys.stdin.fileno()

    # 获取标准输入(终端)的设置
    old_ttyinfo = termios.tcgetattr(fd)

    # 配置终端
    new_ttyinfo = old_ttyinfo[:]

    # 使用非规范模式(索引3是c_lflag 也就是本地模式)
    new_ttyinfo[3] &= ~termios.ICANON

    # 关闭回显(输入不会被显示)
    # new_ttyinfo[3] &= ~termios.ECHO

    # 使设置生效
    termios.tcsetattr(fd, termios.TCSANOW, new_ttyinfo)

    os.read(fd, 2)


def pause():
    print('Press any key to continue...')
    if sys.platform == 'win32':
        pause_windows()
    else:
        pause_linux()


class SingletonWithArgs:
    """带参数的单例模式, 通过继承使用，需放到第一继承位"""

    def __new__(cls, *args, **kwargs):
        arg = '%s%s' % (args, kwargs)
        if not hasattr(cls, '_instances'):
            cls._instances = {}
        if not cls._instances.get(arg):
            cls._instances[arg] = super().__new__(cls)
        return cls._instances[arg]


class ArgMethodBase:
    """auto generator arguments by static methods"""

    def __init__(self, epilog=None):
        """initialize arguments parser"""
        parser = argparse.ArgumentParser(
            description=self.__doc__,
            epilog=epilog,
            formatter_class=argparse.RawDescriptionHelpFormatter,
        )
        subparsers = parser.add_subparsers(title='action', dest='action')
        for arg_map in self.__get_arg_lists__():
            sub_parser = subparsers.add_parser(arg_map['action'], help=arg_map['help'])
            for arg in arg_map['required_args']:
                sub_parser.add_argument(arg)
            for arg, value in arg_map['zip_optional_args']:
                sub_parser.add_argument('--%s' % arg, type=type(value), default=value)

        args = parser.parse_args()
        if args.action is None:
            parser.print_help()
        else:
            if self.__run__(**vars(args)) is False:
                print(color('ERROR', 'red'))
                exit(1)
            print(color('OK', 'green'))

    def __run__(self, action, **args):
        """run a certain staticmethod"""
        return getattr(self, action)(**args)

    def __get_arg_lists__(self):
        """get arguments info lists from self class staticmethods"""
        arg_lists = []

        for func_name in dir(self):
            func = getattr(self, func_name)
            if func_name.startswith('__') or not callable(func):
                continue
            default_len = 0
            default_values = []
            if func.__defaults__ is not None:
                default_len = len(func.__defaults__)
                default_values = func.__defaults__
            required_args = func.__code__.co_varnames[: func.__code__.co_argcount - default_len]
            optional_args = func.__code__.co_varnames[
                func.__code__.co_argcount - default_len : func.__code__.co_argcount
            ]
            arg_lists.append(
                {
                    'action': func_name,
                    'help': func.__doc__,
                    'required_args': required_args,
                    'zip_optional_args': zip(optional_args, default_values),
                }
            )
        return arg_lists


def timeout_windows(seconds):
    import msvcrt

    for second in range(seconds, 0, -1):
        if msvcrt.kbhit():
            print('nit')
            return
        print(f'Waiting {second}s , press any key to continue...', end='\r')
        time.sleep(1)


def timeout(seconds):
    if sys.platform == 'win32':
        timeout_windows(seconds)
    else:
        timeout_linux(seconds)


def timeout_linux(seconds):
    import select
    import termios
    import tty

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
    timeout(5)
