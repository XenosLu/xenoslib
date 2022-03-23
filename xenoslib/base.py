#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import sys
import time


def sleep(seconds, mute=False):
    """sleep with countdown show and prevent pause or sleep of PC"""
    end = time.time() + seconds
    while time.time() < end:
        if not mute:
            print(f'Remaining {seconds:.0f}/{end - time.time():.0f}  s\t', end='\r')
        time.sleep(0.001)


def color(value, color_name='blue'):
    """
    return text with color, default in blue.
    "Why is it blue?"
    "It's always blue."
    """
    if sys.platform == 'win32':
        return value
    color_code = {
        'red': 31,
        'green': 32,
        'yellow': 33,
        'blue': 34,
        'magenta': 35,
        'cyan': 36,
    }
    return '\033[1;{code}m{value}\033[0m'.format(code=color_code[color_name], value=value)


class NestedData:
    """utils for nested data"""

    def __init__(self, obj):
        self.data = obj

    def _find_key(self, obj, path=''):
        if isinstance(obj, dict):
            for k, v in obj.items():
                new_path = f"{path}['{k}']"
                if k == self.key:
                    self.path = new_path
                    return v
                else:
                    ret = self._find_key(v, new_path)
                    if ret is not None:
                        return ret
        elif isinstance(obj, list):
            for n, i in enumerate(obj):
                ret = self._find_key(i, f'{path}[{n}]')
                if ret is not None:
                    return ret
        return None

    def _find_value(self, obj, path=''):
        if isinstance(obj, dict):
            for k, v in obj.items():
                new_path = f"{path}['{k}']"
                if v == self.value:
                    self.path = new_path
                    return obj
                else:
                    ret = self._find_value(v, new_path)
                    if ret is not None:
                        return ret
        elif isinstance(obj, list):
            for n, i in enumerate(obj):
                new_path = f'{path}[{n}]'
                ret = self._find_value(i, new_path)
                if i == self.value:
                    self.path = new_path
                    return obj
                if ret is not None:
                    return ret
        return None

    def _find_key_value(self, obj, path=''):
        if isinstance(obj, dict):
            for k, v in obj.items():
                new_path = f"{path}['{k}']"
                if k == self.key and v == self.value:
                    self.path = new_path
                    return obj
                else:
                    ret = self._find_key_value(v, new_path)
                    if ret is not None:
                        return ret
        elif isinstance(obj, list):
            for n, i in enumerate(obj):
                ret = self._find_key_value(i, f'{path}[{n}]')
                if ret is not None:
                    return ret
        return None

    def find_key(self, key):
        """find key and path for data"""
        self.path = None
        self.key = key
        return self._find_key(self.data)

    def find_value(self, value):
        """find data that matches value and path for data"""
        self.path = None
        self.value = value
        return self._find_value(self.data)

    def find_keyvalue(self, key, value):
        """find data matches both key and value"""
        self.path = None
        self.key = key
        self.value = value
        return self._find_key_value(self.data)


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
