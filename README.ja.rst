~~~~~~~
jj-menu
~~~~~~~

シンプル CUI (TUI) メニュー

.. image:: demo/jj-demo.gif

インストール
---------------------------------------
::

  $ pip install git+https://github.com/ytyng/jj-menu.git


設定
---------------------------------------

**jjfile.py** を作る

もしくは jjfile/__init__.py

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

menu 変数がメニューとなります。
実行するディレクトリと、親ディレクトリを再帰的に探します。


シェル関数の登録 (Bash) (オプション)

::

    function jj(){
        RESULT_FILE=/tmp/_jj_result
        jj-menu --result-file=${RESULT_FILE}
        if [ $? == 0 ]; then
            source ${RESULT_FILE}
            history -s `cat ${RESULT_FILE}`
        fi
    }


実行
---------------------------------------

::

  $ jj

上記 jj シェル関数を登録してある場合、jj で現在のシェルプロセス上で選択したコマンドを実行します。

jj シェル関数を登録していない場合は、

::

  $ jj-menu

で、メニュー選択したコマンドを子プロセスで実行します。
この、子プロセスで実行する場合は、cd したり シェル変数を書き換えたりのコマンドは意味がなくなります。


Key binds
---------

::

    ESC: Exit
    Q: Exit
    k: Up
    j: Down
