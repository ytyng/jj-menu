#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import curses

colors = {
    2: curses.COLOR_YELLOW,
    3: (curses.COLOR_BLUE, curses.COLOR_WHITE),
}

menu = [
    ('Launch editor', 'open -a PyCharm .'),
    ('Build package', 'python setup.py sdist', {"color": 2}),
    ('Upload package', 'twine upload dist/*', {"color": 3}),
    ('Test', 'python setup.py test'),
    ('Git logs (simple)',
     'git log --graph --date-order -C -M '
     '--pretty=format:"<%h> %ad [%an] %Cgreen%d%Creset %s" '
     '--all --date=short'),
    ('Git logs (verbose)',
     'git log --graph --date=iso --decorate --name-status'),
    ('Copy datetime to pasteboard',
     'date +"%Y-%m-%d %H:%M:%S"|pbcopy')
]
