#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name='xenoslib',
    version='0.1.2.3',
    packages=find_packages(),
    description="Xenos' common lib",
    author='Xenocider',
    author_email='xenos.lu@gmail.com',
    url='https://github.com/XenosLu/xenoslib.git',
    install_requires=['PyYAML>=5.1'],
    python_requires='>=3.4.0',
)
