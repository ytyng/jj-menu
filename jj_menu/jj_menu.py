#!/usr/bin/env python
# -*- coding:utf-8 -*-

from __future__ import unicode_literals, print_function
import os
import sys
import locale
import curses
import _curses
import six

# 文字化け対応
locale.setlocale(locale.LC_ALL, '')

COLOR_ACTIVE = 1

result_filename = '/tmp/_jj_result'


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
    # Get directory and fabfile name
    dir_name, file_name = os.path.split(menu_file_path)
    if dir_name not in sys.path:
        sys.path.insert(0, dir_name)
    imported = importer(os.path.splitext(file_name)[0])
    return imported


def get_menu():
    def _get_menus():
        """
        メニュー項目1つなら同じものに展開
        """
        menus = getattr(import_menu_settings(), 'menu')
        for m in menus:
            if isinstance(m, str):
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
    def __init__(self, stdscr):
        stdscr.refresh()  # なにより先にまず1回リフレッシュ
        self.stdscr = stdscr
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
        簡易デバッグ
        """
        win = curses.newwin(1, 10, self.max_y - 2, self.max_x - 10)
        window_addstr(win, 0, 0, message[:10])
        win.refresh()

    def serve(self):
        while True:

            self.render()

            # キー入力待機
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
                # 決定
                with open(result_filename, 'w') as fp:
                    fp.write(self.menu[self.pos_y][1])
                return self.menu[self.pos_y]
            else:
                self.debug('{}'.format(c))

    def init_outfile(self):
        with open(result_filename, 'w') as fp:
            fp.write('')


def launch(stdscr):
    initialize_colors()
    _curses.curs_set(0)
    # 画面サイズ取得
    launcher = Launcher(stdscr)

    selected = launcher.serve()
    return selected


def main():
    try:
        selected = curses.wrapper(launch)
        print('$ {}'.format(selected[1]))
    except KeyboardInterrupt:
        exit(1)


if __name__ == '__main__':
    main()
