#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

menu = [
    ('list python processes', 'ps -eafw|grep python'),
    ('move tmp', 'cd /tmp/'),
    ('list dirs', ['ls .', 'ls ..', 'ls ../..']),
    ('Git logs (simple)',
     'git log --graph --date-order -C -M --pretty=format:"<%h> %ad [%an] %Cgreen%d%Creset %s" '
     '--all --date=short'),
    ('Git logs (verbose)',
     'git log --graph --date=iso --decorate --name-status'),
    ('Copy datetime to pasteboard',
     'date +"%Y-%m-%d %H:%M:%S"|pbcopy')
]
