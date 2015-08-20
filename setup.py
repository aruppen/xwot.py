#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

VERSION = "1.0.1"

setup(
    name="xwot",
    packages=find_packages('.', exclude=["tests", "test"]),
    entry_points={
        'console_scripts': [
            'xwotc = xwot.cmd:xwotc',
            'xwotd = xwot.cmd:xwotd',
#            'xwotp2v = xwot.cmd:xwotp2v'
        ]
    },
    version=VERSION,
    install_requires=['dicttoxml==1.6.6', 'xmltodict==0.9.2'],
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
