#!/usr/bin/env python
# coding: utf-8
from setuptools import setup
from jj_menu import __author__, __version__, __license__

setup(
    name='jj-menu',
    version=__version__,
    description='Simple CUI (TUI) Launcher menu',
    license=__license__,
    author=__author__,
    author_email='ytyng@live.jp',
    url='https://github.com/ytyng/jj-menu.git',
    keywords='CUI, TUI, Launcher, Python, curses',
    packages=['jj_menu'],
    install_requires=['six'],
    entry_points={
        'console_scripts': [
            'jj-menu = jj_menu.jj_menu:main',
        ]
    },
)
