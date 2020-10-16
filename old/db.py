import sqlite3


def ensure_connection(func):
    """ Декоратор для подключения к СУБД: открывает соединение,
        выполняет переданную функцию и закрывает за собой соединение.
        Потокобезопасно!
    """
    def inner(*args, **kwargs):
        with sqlite3.connect('users_bot.db') as conn:
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
            id               INTEGER PRIMARY KEY,
            user_id          INTEGER NOT NULL,
            user_name        TEXT,
            subscribe        INTEGER NOT NULL DEFAULT 0,
            latitude         REAL NOT NULL DEFAULT 50.479211,
            longitude        REAL NOT NULL DEFAULT 30.434911,
            time_notify      TEXT
        )
    ''')

    # Сохранить изменения
    conn.commit()

@ensure_connection
def add_user_in_db(conn, user_id: int, user_name: str):
    c = conn.cursor()
    c.execute('INSERT INTO bot_users (user_id, user_name) VALUES (?, ?)', (user_id, user_name))
    conn.commit()

@ensure_connection
def check_in_db(conn, column, data_check):
    c = conn.cursor()
    c.execute(f'SELECT {column} FROM bot_users WHERE {column}=?', [data_check])
    return c.fetchone()
    # if c.fetchone():
    #     return True
    # else:
    #     return False

@ensure_connection
def subscribe_db(conn, user_id: int):
    c = conn.cursor()
    c.execute(f'UPDATE bot_users SET subscribe=1 WHERE user_id = {user_id}')
    conn.commit()

@ensure_connection
def check_subscribe_db(conn, user_id: int):
    c = conn.cursor()
    c.execute(f'SELECT subscribe FROM bot_users WHERE user_id=?', [user_id])
    if c.fetchone()[0]:
        return True
    else:
        return False

@ensure_connection
def unsubscribe_db(conn, user_id: int):
    c = conn.cursor()
    c.execute(f'UPDATE bot_users SET subscribe=0 WHERE user_id = {user_id}')
    conn.commit()

@ensure_connection
def set_time_notify(conn, user_id: int, time: str):
    c = conn.cursor()
    c.execute(f'UPDATE bot_users SET time_notify=? WHERE user_id = {user_id}', [time])
    conn.commit()

@ensure_connection
def list_id_users_in_db(conn):
    c = conn.cursor()
    c.execute(f'SELECT * FROM bot_users')
    return c.fetchall()

@ensure_connection
def get_time_notify_user_db(conn, user_id: int):
    c = conn.cursor()
    c.execute(f'SELECT time_notify FROM bot_users WHERE user_id=?', [user_id])
    return c.fetchone()[0]

@ensure_connection
def set_geoposition(conn, user_id: int, latit: float, long: float):
    c = conn.cursor()
    c.execute(f'UPDATE bot_users SET latitude={latit} WHERE user_id = {user_id}')
    c.execute(f'UPDATE bot_users SET longitude={long} WHERE user_id = {user_id}')
    conn.commit()

@ensure_connection
def get_geoposition(conn, user_id: int):
    c = conn.cursor()
    c.execute(f'SELECT latitude FROM bot_users WHERE user_id=?', [user_id])
    latitude = c.fetchone()[0]
    c.execute(f'SELECT longitude FROM bot_users WHERE user_id=?', [user_id])
    longitude = c.fetchone()[0]
    return latitude, longitude

@ensure_connection
def count_users(conn):
    c = conn.cursor()
    c.execute(f'SELECT COUNT(*) FROM bot_users')
    users = c.fetchone()[0]
    return users


if __name__ == '__main__':
    init_db(force=True)