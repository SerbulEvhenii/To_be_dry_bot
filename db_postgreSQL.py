# файл описывает всю логику работы с БД
from typing import List

import psycopg2
import os

from psycopg2.sql import SQL, Identifier

DATABASE_URL = os.environ['DATABASE_URL']


def ensure_connection(func):
    """ Декоратор для подключения к СУБД: открывает соединение,
        выполняет переданную функцию и закрывает за собой соединение.
        Потокобезопасно!
    """

    def inner(*args, **kwargs):
        with psycopg2.connect(DATABASE_URL, sslmode='require') as conn:
            kwargs['conn'] = conn
            res = func(*args, **kwargs)
        return res

    return inner


@ensure_connection
def init_db(conn, force: bool = False):
    """ Проверить что нужные таблицы существуют, иначе создать их

        :param conn: подключение к СУБД
        :param force: явно пересоздать все таблицы
    """
    c = conn.cursor()

    if force:
        c.execute('DROP TABLE IF EXISTS bot_users')

    c.execute('''
        CREATE TABLE IF NOT EXISTS bot_users (
            id               SERIAL PRIMARY KEY,
            user_id          INTEGER NOT NULL,
            user_name        TEXT,
            subscribe        INTEGER NOT NULL DEFAULT 0,
            latitude         REAL NOT NULL DEFAULT 50.479211,
            longitude        REAL NOT NULL DEFAULT 30.434911,
            time_notify      TEXT,
            city             CHARACTER VARYING(50) NOT NULL DEFAULT 'Киев, Украина'
        )
    ''')

    # Сохранить изменения
    conn.commit()


@ensure_connection
def add_user_in_db(conn, user_id: int, user_name: str):
    c = conn.cursor()
    c.execute('INSERT INTO bot_users (user_id, user_name) VALUES (%s, %s)', (user_id, user_name))
    conn.commit()


@ensure_connection
def check_in_db_user(conn, data_check) -> bool:
    c = conn.cursor()
    c.execute('SELECT user_id FROM bot_users WHERE user_id= %s', [data_check])
    return c.fetchone()


@ensure_connection
def subscribe_db(conn, user_id: int):
    c = conn.cursor()
    # c.execute(f'UPDATE bot_users SET subscribe=1 WHERE user_id = {user_id}')
    c.execute('UPDATE bot_users SET subscribe=1 WHERE user_id = %s', [user_id])
    conn.commit()


@ensure_connection
def check_subscribe_db(conn, user_id: int) -> bool:
    c = conn.cursor()
    # c.execute(f'SELECT subscribe FROM bot_users WHERE user_id={user_id}')
    c.execute('SELECT subscribe FROM bot_users WHERE user_id= %s', [user_id])
    if c.fetchone()[0]:
        return True
    else:
        return False


@ensure_connection
def unsubscribe_db(conn, user_id: int):
    c = conn.cursor()
    # c.execute(f'UPDATE bot_users SET subscribe=0 WHERE user_id = {user_id}')
    c.execute('UPDATE bot_users SET subscribe=0 WHERE user_id = %s', [user_id])
    conn.commit()


@ensure_connection
def set_time_notify(conn, user_id: int, time: str):
    c = conn.cursor()
    c.execute('UPDATE bot_users SET time_notify=%s WHERE user_id = %s;', (time, user_id))
    conn.commit()


@ensure_connection
def list_id_users_in_db(conn) -> List:
    c = conn.cursor()
    c.execute('SELECT * FROM bot_users')
    return c.fetchall()


@ensure_connection
def get_time_notify_user_db(conn, user_id: int) -> str:
    c = conn.cursor()
    c.execute('SELECT time_notify FROM bot_users WHERE user_id=%s;', [user_id])
    try:
        return c.fetchone()[0]
    except IndexError:
        return ''


@ensure_connection
def set_geoposition(conn, user_id: int, latit: float, long: float):
    c = conn.cursor()
    # c.execute(f'UPDATE bot_users SET latitude={latit} WHERE user_id = {user_id}')
    # c.execute(f'UPDATE bot_users SET longitude={long} WHERE user_id = {user_id}')
    c.execute('UPDATE bot_users SET latitude=%s WHERE user_id = %s', (latit, user_id))
    c.execute('UPDATE bot_users SET longitude=%s WHERE user_id = %s', (long, user_id))
    conn.commit()


@ensure_connection
def get_geoposition(conn, user_id: int):
    c = conn.cursor()
    c.execute('SELECT latitude FROM bot_users WHERE user_id=%s;', [user_id])
    latitude = c.fetchall()[0][0]
    c.execute('SELECT longitude FROM bot_users WHERE user_id=%s;', [user_id])
    longitude = c.fetchall()[0][0]
    return latitude, longitude


@ensure_connection
def set_city_user_db(conn, user_id: int, geopy_city):
    c = conn.cursor()
    c.execute('UPDATE bot_users SET city=%s WHERE user_id=%s;', (geopy_city, user_id))
    conn.commit()


@ensure_connection
def get_city_user_db(conn, user_id: int) -> str:
    c = conn.cursor()
    c.execute('SELECT city FROM bot_users WHERE user_id=%s;', [user_id])
    return c.fetchone()[0]


@ensure_connection
def count_users(conn) -> int:
    c = conn.cursor()
    c.execute('SELECT COUNT(*) FROM bot_users')
    return c.fetchone()[0]

