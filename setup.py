#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name='xenoslib',
    version='0.1.11.0',
    packages=find_packages(),
    description="Xenos' common lib",
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
