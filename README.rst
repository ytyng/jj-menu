~~~~~~~
jj-menu
~~~~~~~

Simple CLI Menu


Install
-------
::

  $ pip install git+https://github.com/ytyng/jj-menu.git


Setup
-----

Create jjfile.py into any directory.

::

    menu = [
        ('list python processes', 'ps -eafw|grep python'),
        ('move tmp', 'cd /tmp/'),
        ('list dirs', ['ls .', 'ls ..', 'ls ../..']),
    ]

Run
---

::

  $ jj


Key binds
---------

ESC: Exit
Q: Exit
k: Up
j: Down
