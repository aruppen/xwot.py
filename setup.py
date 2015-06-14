#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

VERSION = "0.1.0"

setup(
    name="xwot",
    packages=find_packages('.'),
    entry_points={
        'console_scripts': [
            'xwotc = xwot.cmd:xwotc',
            'xwotd = xwot.cmd:xwotd'
        ]
    },
    version=VERSION,
    description="xwot",
    author="Alexander Rüedlinger",
    author_email="a.rueedlinger@gmail.com",
    license="MIT",
    classifiers=[],
    ext_modules=[],
    long_description="""\
xWoT
-------------------------------------


"""
)