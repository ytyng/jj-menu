#!/usr/bin/env python
# -*- coding:utf-8 -*-

from __future__ import unicode_literals, print_function

import argparse
import os
import sys
import locale
import curses
import _curses
import subprocess
import six

locale.setlocale(locale.LC_ALL, '')

COLOR_ACTIVE = 1


HELP = """jjfile.py not found. Create it into current or parent directory.
sample:
----------------------------------------------------------
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
----------------------------------------------------------

... and create shell function:
----------------------------------------------------------
function jj(){
    RESULT_FILE=/tmp/_jj_result
    jj-menu --result-file=${RESULT_FILE}
    if [ $? == 0 ]; then
        history -s `cat ${RESULT_FILE}`
        source ${RESULT_FILE}
    fi
}

"""


class MenuFileNotFound(Exception):
    pass


def initialize_colors():
    curses.use_default_colors()
    curses.init_pair(COLOR_ACTIVE, curses.COLOR_BLACK, curses.COLOR_WHITE)


def find_menu_file_path(cwd):
    paths = [
        os.path.join(cwd, 'jjfile'),
        os.path.join(cwd, 'jjfile.py'), ]
    for p in paths:
        if os.path.exists(p):
            return p
    parent_dir = os.path.dirname(cwd)
    if parent_dir == cwd:
        raise MenuFileNotFound()
    else:
        return find_menu_file_path(parent_dir)


def import_menu_settings():
    menu_file_path = find_menu_file_path(os.getcwd())

    importer = __import__
    dir_name, file_name = os.path.split(menu_file_path)
    if dir_name not in sys.path:
        sys.path.insert(0, dir_name)
    imported = importer(os.path.splitext(file_name)[0])
    return imported


def get_menu():
    def _get_menus():
        menus = getattr(import_menu_settings(), 'menu')
        for m in menus:
            if isinstance(m, six.string_types):
                yield (m, m)
            elif len(m) >= 2:
                if isinstance(m[1], (list, tuple)):
                    yield (m[0], ";".join(m[1]))
                else:
                    yield m

    return list(_get_menus())


def window_addstr(window, y, x, message, color=None):
    """
    python 2, 3 multi-bytes compatible
    """
    if six.PY2:
        new_message = message.encode('utf-8')
    else:
        new_message = message
    args = [y, x, new_message]
    if color is not None:
        args.append(color)
    try:
        window.addstr(*args)
    except _curses.error:
        pass
        # print(e)


class Launcher(object):
    def __init__(self, stdscr, result_file=None):
        stdscr.refresh()
        self.stdscr = stdscr
        self.result_file = result_file
        self.max_y, self.max_x = stdscr.getmaxyx()
        self.pos_y = 0
        self.menu = get_menu()
        self.init_outfile()

    def render(self):
        win = curses.newwin(
            len(self.menu), self.max_x, 0, 0)
        for y, item in enumerate(self.menu):
            item_name_str = item[0]
            if y == self.pos_y:
                window_addstr(
                    win, y, 0, '*> {}'.format(item_name_str),
                    curses.color_pair(COLOR_ACTIVE))
            else:
                window_addstr(
                    win, y, 0, '   {}'.format(item_name_str))
        win.refresh()
        # win.refresh(0, 0, 0, 0, len(MENU), self.max_x)

        help_win = curses.newwin(1, self.max_x, self.max_y - 1, 0)
        message = '$ {}'.format(self.menu[self.pos_y][1])
        window_addstr(
            help_win, 0, 0, message[:self.max_x - 1],
            curses.color_pair(COLOR_ACTIVE))
        help_win.refresh()

    def debug(self, message):
        """
        Easy debug
        """
        win = curses.newwin(1, 10, self.max_y - 2, self.max_x - 10)
        window_addstr(win, 0, 0, message[:10])
        win.refresh()

    def serve(self):
        while True:

            self.render()

            # Waiting key input
            c = self.stdscr.getch()

            if c in (14, 106, 258):  # ↓
                if self.pos_y < len(self.menu) - 1:
                    self.pos_y += 1

            elif c in (16, 107, 259):  # ↑
                if self.pos_y > 0:
                    self.pos_y -= 1

            elif c in (2, 104, 260):  # ←
                pass

            elif c in (6, 108, 261):  # →
                pass
            elif c in (113, 27):  # Q, Esc
                raise KeyboardInterrupt()
            elif c == 10:
                # choose
                script = self.menu[self.pos_y][1]
                if self.result_file:
                    with open(self.result_file, 'w') as fp:
                        fp.write(script)
                return script
            else:
                self.debug('{}'.format(c))

    def init_outfile(self):
        if not self.result_file:
            return
        with open(self.result_file, 'w') as fp:
            fp.write('')


def launch(stdscr, args):
    initialize_colors()
    _curses.curs_set(0)
    launcher = Launcher(stdscr, result_file=args.result_file)

    return launcher.serve()


def main():
    parser = argparse.ArgumentParser(description='jj-menu core')
    parser.add_argument('--result-file', dest='result_file',
                        help='result script file path', default=None)

    args = parser.parse_args()

    try:
        script = curses.wrapper(launch, args)
        print('$ {}'.format(script))
        if not args.result_file:
            print(subprocess.check_output(script, shell=True))

    except MenuFileNotFound:
        print_help()
        exit(1)
    except KeyboardInterrupt:
        exit(1)


def print_help():
    print(HELP)

if __name__ == '__main__':
    main()
