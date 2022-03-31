#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
from xenoslib import __version__

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
        'requests>=2',
    ],
    python_requires='>=3.5.0',
    extras_require={
        ':sys_platform == "win32"': ['pywin32>=223'],
        ':"linux" in sys_platform': [],
    },
)
