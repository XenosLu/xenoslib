#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse

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
        return '\033[1;{code}m{value}\033[0m'.format(
            code=color_code[color_name], value=value)

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
            description=self.__doc__, epilog=epilog,
            formatter_class=argparse.RawDescriptionHelpFormatter)
        subparsers = parser.add_subparsers(title='action', dest='action')
        for arg_map in self.__get_arg_lists__():
            sub_parser = subparsers.add_parser(
                arg_map['action'], help=arg_map['help'])
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
            required_args = func.__code__.co_varnames[:
                                                      func.__code__.co_argcount - default_len]
            optional_args = func.__code__.co_varnames[func.__code__.co_argcount -
                                                      default_len:func.__code__.co_argcount]
            arg_lists.append({
                'action': func_name,
                'help': func.__doc__,
                'required_args': required_args,
                'zip_optional_args': zip(optional_args, default_values),
            })
        return arg_lists