#!/usr/bin/env python
# coding: utf-8
from setuptools import setup, find_packages
from jj_menu import __author__, __version__, __license__

install_requires=['curses', 'six']

setup(
    name='jj-menu',
    version=__version__,
    description='Simple CLI Menu',
    license=__license__,
    author=__author__,
    author_email='ytyng@live.jp',
    url='https://github.com/jytyng/jj-menu.git',
    keywords='CLI Menu, Python',
    packages=find_packages(),
    install_requires=[],
)
