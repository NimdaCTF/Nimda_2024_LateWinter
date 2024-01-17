import sqlite3
from hashlib import md5
from string import ascii_lowercase, digits
from random import choice, randint
import os


def get_random_str(length: int):
    return ''.join([choice(ascii_lowercase + digits) for _ in range(length)])


def generate():
    if os.path.exists('db.sqlite3'):
        os.remove('db.sqlite3')

    connection = sqlite3.connect('db.sqlite3')
    cursor = connection.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password TEXT NOT NULL
    )
    ''')

    connection.commit()

    logins = []

    for _ in range(500):
        login = get_random_str(randint(6, 12))
        logins.append(login)
        password = md5(get_random_str(4).encode()).hexdigest()
        cursor.execute(f'INSERT INTO Users VALUES (NULL, \'{login}\', \'{password}\')')

    connection.commit()
    connection.close()

    with open('admin', 'w', encoding='UTF-8') as f:
        f.write(choice(logins))


if __name__ == '__main__':
    generate()
