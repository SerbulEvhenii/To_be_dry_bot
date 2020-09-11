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

        Важно: миграции на такие таблицы вы должны производить самостоятельно!

        :param conn: подключение к СУБД
        :param force: явно пересоздать все таблицы
    """
    c = conn.cursor()

    # Информация о пользователе
    # TODO: создать при необходимости...

    # Сообщения от пользователей
    if force:
        c.execute('DROP TABLE IF EXISTS bot_users')

    c.execute('''
        CREATE TABLE IF NOT EXISTS bot_users (
            id               INTEGER PRIMARY KEY,
            user_id          INTEGER NOT NULL,
            user_name        TEXT NOT NULL,
            subscribe        NUMERIC
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
    if c.fetchone():
        return True
    else:
        return False

@ensure_connection
def subscribe_db(conn, user_id: int):
    c = conn.cursor()
    c.execute('UPDATE bot_users SET subscribe = 1 WHERE user_id = user_id')
    conn.commit()

@ensure_connection
def unsubscribe_db(conn, user_id: int):
    c = conn.cursor()
    c.execute('UPDATE bot_users SET subscribe = 0 WHERE user_id = user_id')
    conn.commit()


# # Create cursor object
# cur = users_bot.db.cursor()
#
# # run a select query against the table to see if any record exists
# # that has the email or username
# cur.execute("""SELECT email
#                       ,username
#                FROM users
#                WHERE email=?
#                    OR username=?""",
#             (email, username))
#
# # Fetch one result from the query because it
# # doesn't matter how many records are returned.
# # If it returns just one result, then you know
# # that a record already exists in the table.
# # If no results are pulled from the query, then
# # fetchone will return None.
# result = cur.fetchone()
#
# if result:
#     # Record already exists
#     # Do something that tells the user that email/user handle already exists
# else:
#     cur.execute("INSERT INTO users VALUES (?, ?, ?)", (email, username, password))
#     g.db.commit()

if __name__ == '__main__':
    init_db(force=True)
