from bot import bot  # Импортируем объект бота
from messages import *  # Инмпортируем все с файла сообщений
from db import *

@bot.message_handler(commands=['start'])
# Выполняется, когда пользователь вызывает /start
def send_welcome(message):
    if check_in_db(column='user_id', data_check=message.chat.id):
        bot.send_message(message.chat.id, f'{HELLO_AGAIN_MESSAGE}, {message.chat.first_name}!')
    else:
        add_user_in_db(user_name=message.chat.username, user_id=message.chat.id)
        bot.send_message(message.chat.id,
                         f'Привет, {message.chat.first_name}.\n'
                         f'Я погодный Бот! Я буду оповещать тебя, если в ближайшее время в твоем городе будет идти '
                         f'дождь.')


@bot.message_handler(commands=['subs'])
# Выполняется, когда пользователь вызывает /subs
def subscribe(message):
    if check_subscribe_db(user_id=message.chat.id):
        bot.send_message(message.chat.id, SUBSCRIBE_IS)
    else:
        subscribe_db(user_id=message.chat.id)
        bot.send_message(message.chat.id, SUBSCRIBE)


@bot.message_handler(commands=['unsubs'])
# Выполняется, когда пользователь вызывает /unsubs
def unsubscribe(message):
    unsubscribe_db(user_id=message.chat.id)
    bot.send_message(message.chat.id, UNSUBSCRIBE)


@bot.message_handler(content_types=["text"])  # Любой текст
def repeat_all_messages(message):
    bot.send_message(message.chat.id, message.text)


if __name__ == '__main__':
    init_db()
    bot.polling(none_stop=True)
