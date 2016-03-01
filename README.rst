~~~~~~~
jj-menu
~~~~~~~

Simple CUI (TUI) Menu

.. image:: demo/jj-demo.gif

Install
-------
::

  $ pip install jj-menu

( or $ pip install git+https://github.com/ytyng/jj-menu.git )


Setup
-----

Create **jjfile.py** into any directory.

::

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

And register shell function (Optional)

::

    function jj(){
        RESULT_FILE=/tmp/_jj_result
        jj-menu --result-file=${RESULT_FILE}
        if [ $? == 0 ]; then
            history -s `cat ${RESULT_FILE}`
            source ${RESULT_FILE}
        fi
    }

Run
---

::

  $ jj

or

::

  $ jj-menu

(In not registered jj shell function. Run selected command in subprocess.)

Key binds
---------

::

    ESC: Exit
    Q: Exit
    k: Up
    j: Down
