#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'xenoslib'))
from version import __version__  # noqa

setup(
    name='xenoslib',
    version=__version__,
    packages=find_packages(),
    description="Xenos' common lib",
    long_description_content_type='text/x-rst',
    author='Xenocider',
    author_email='xenos.lu@gmail.com',
    url='https://github.com/XenosLu/xenoslib.git',
    install_requires=[
        'PyYAML>=5.4',
    ],
    python_requires='>=3.6',
    extras_require={
        ':sys_platform == "win32"': ['pywin32>=225'],
        ':python_version >= "3.10"': ['requests>=2.19'],
        ':python_version <= "3.9"': ['requests>=2.0.0'],
        'colorful:sys_platform == "win32"': ['colorama>=0.4.4'],
        ':"linux" in sys_platform': [],
    },
    tests_require=['pytest>=2.8.0'],
)
