import sqlite3
from datetime import datetime

connection = sqlite3.connect('MultiTool.db')
sql = connection.cursor()

sql.execute('CREATE TABLE IF NOT EXISTS users'
            '(tg_id INTEGER, nickname TEXT, name TEXT, surname TEXT, username TEXT,'
            'menu_type TEXT, reg_date DATETIME);')


def register_user(tg_id, nickname, name, surname, username, menu_type):
    connection = sqlite3.connect('MultiTool.db')
    sql = connection.cursor()

    sql.execute('INSERT INTO users'
                '(tg_id, nickname, name, surname, username, menu_type, reg_date)'
                'VALUES (?, ?, ?, ?, ?, ?, ?);',
                (tg_id, nickname, name, surname, username, menu_type, datetime.now()))

    connection.commit()


def check_user(user_id):
    connection = sqlite3.connect('MultiTool.db')
    sql = connection.cursor()

    checker = sql.execute('SELECT tg_id FROM users '
                          'WHERE tg_id=?;', (user_id,))

    return checker.fetchone()


def user_menu_view(user_id):
    connection = sqlite3.connect('MultiTool.db')
    sql = connection.cursor()

    menu_view = sql.execute('SELECT menu_type FROM users '
                            'WHERE tg_id=?;',
                            (user_id,)).fetchone()

    return menu_view[0]


def swap_user_menu_view(user_id, old_user_menu_view):
    connection = sqlite3.connect('MultiTool.db')
    sql = connection.cursor()

    if old_user_menu_view == 'text':
        new_user_menu_view = 'buttons'
    else:
        new_user_menu_view = 'text'

    sql.execute('UPDATE users SET menu_type=? '
                'WHERE tg_id=?;',
                (new_user_menu_view, user_id))

    connection.commit()


def get_nickname(user_id):
    connection = sqlite3.connect('MultiTool.db')
    sql = connection.cursor()

    nickname = sql.execute('SELECT nickname FROM users '
                           'WHERE tg_id=?;',
                           (user_id,)).fetchone()

    return nickname[0]
