#!/usr/bin/env python
# coding: utf-8
from setuptools import setup, find_packages
from jj_menu import __author__, __version__, __license__

# In [2]: from setuptools.command.bdist_egg import _get_purelib
#
# In [3]: _get_purelib()
# Out[3]: '/Users/yotsuyanagi/.virtualenvs/default/lib/python2.7/site-packages'
# $ cd $(python -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())"

setup(
    name='jj-menu',
    version=__version__,
    description='Simple CUI (TUI) Launcher menu',
    license=__license__,
    author=__author__,
    author_email='ytyng@live.jp',
    url='https://github.com/ytyng/jj-menu.git',
    keywords='CUI, TUI, Launcher, Python, curses',
    packages=find_packages(),
    install_requires=['six'],
    entry_points={
        'console_scripts': [
            'jj-menu = jj_menu.jj_menu:main',
        ]
    },
)
