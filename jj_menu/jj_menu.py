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

ACTIVE_COLOR_PAIR_ID = ACTIVE_COLOR_OFFSET = 256

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
     'git log --graph --date-order -C -M --pretty=format:"<%h> %ad [%an] '
     '%Cgreen%d%Creset %s" --all --date=short'),
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


class ColorIdTooLarge(Exception):
    pass


def initialize_colors():
    # curses.start_color()
    curses.use_default_colors()
    curses.init_pair(ACTIVE_COLOR_PAIR_ID,
                     curses.COLOR_BLACK, curses.COLOR_WHITE)


def setup_color_palette(color_dict):
    if not color_dict:
        return
    for color_pair_id, color_setting in color_dict.items():
        if color_pair_id >= 255:
            raise ColorIdTooLarge(color_pair_id)
        if isinstance(color_setting, (list, tuple)):
            fg_color, bg_color = color_setting
        else:
            fg_color = color_setting
            bg_color = curses.COLOR_BLACK
        curses.init_pair(color_pair_id, fg_color, bg_color)
        curses.init_pair(color_pair_id + ACTIVE_COLOR_OFFSET, bg_color,
                         fg_color)


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


class MenuItem(object):
    def __init__(self, name, command=None, options=None):
        self.name = name
        self.command = self._make_command(command) or name
        self.options = options or {}

    def _make_command(self, command):
        if not command:
            return None
        if isinstance(command, (list, tuple)):
            return ';'.join(command)
        else:
            return command

    @classmethod
    def items(cls, menu_source):
        def _get_menu_items():
            for m in menu_source:
                if isinstance(m, six.string_types):
                    m = [m]
                yield cls(*m)

        return list(_get_menu_items())

    @property
    def default_color_pair_id(self):
        return self.options.get('color', None)

    @property
    def active_color_pair_id(self):
        dci = self.default_color_pair_id
        if not dci:
            return None
        return dci + ACTIVE_COLOR_OFFSET


def window_addstr(window, y, x, message, color_pair_id=None):
    """
    python 2, 3 multi-bytes compatible
    """
    if six.PY2:
        new_message = message.encode('utf-8')
    else:
        new_message = message
    args = [y, x, new_message]
    if color_pair_id is not None:
        args.append(curses.color_pair(color_pair_id))
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
        self.jjfile_module = import_menu_settings()
        self.menu_items = MenuItem.items(
            getattr(self.jjfile_module, 'menu'))
        self.init_outfile()

        setup_color_palette(getattr(
            self.jjfile_module, 'colors', None))

    def render(self):
        win = curses.newwin(
            len(self.menu_items), self.max_x, 0, 0)
        for y, item in enumerate(self.menu_items):
            item_name_str = item.name
            if y == self.pos_y:
                window_addstr(
                    win, y, 0, '*> {}'.format(item_name_str),
                    item.active_color_pair_id or ACTIVE_COLOR_PAIR_ID)
            else:
                window_addstr(
                    win, y, 0, '   {}'.format(item_name_str),
                    item.default_color_pair_id
                )
        win.refresh()
        # win.refresh(0, 0, 0, 0, len(MENU), self.max_x)

        help_win = curses.newwin(1, self.max_x, self.max_y - 1, 0)
        message = '$ {}'.format(self.menu_items[self.pos_y].command)
        window_addstr(
            help_win, 0, 0, message[:self.max_x - 1],
            curses.color_pair(ACTIVE_COLOR_PAIR_ID))
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
                if self.pos_y < len(self.menu_items) - 1:
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
                script = self.menu_items[self.pos_y].command
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
            result = subprocess.check_output(script, shell=True)
            print(result.decode('utf-8', errors='ignore'))

    except MenuFileNotFound:
        print_help()
        exit(1)
    except KeyboardInterrupt:
        exit(1)


def print_help():
    print(HELP)


if __name__ == '__main__':
    main()
