from bot import bot       # Импортируем объект бота
from messages import *    # Инмпортируем все с файла сообщений
from db import *          # Импортируем все методы из файла для базы данных
import weather_api        # Импортируем все методы из файла для погоды
import telebot.types      # Импортируем типы телеграма API
import markups            # Импортируем кнопки для бота


@bot.message_handler(commands=['start'])
# Выполняется, когда пользователь вызывает /start
def send_welcome(message):
    if check_in_db(column='user_id', data_check=message.chat.id):
        bot.send_message(message.chat.id, f'{HELLO_AGAIN_MESSAGE}, {message.chat.first_name}!', reply_markup=markups.markup_main)
    else:
        add_user_in_db(user_name=message.chat.username, user_id=message.chat.id)
        bot.send_message(message.chat.id,
                         f'Привет, {message.chat.first_name}.\n'
                         f'Я погодный Бот! Я буду оповещать тебя, если в ближайшее время в твоем городе будет идти '
                         f'дождь.', reply_markup=markups.markup_main)


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

@bot.message_handler(commands=['time'])
# Выполняется, когда пользователь вызывает /time
def set_time_notify_in_db(message):
    set_time_notify(user_id=message.chat.id, time='07:00')
    bot.send_message(message.chat.id, SET_TIME_NOTIFY)


# @bot.message_handler(content_types=["text"])  # Любой текст
# def repeat_all_messages(message):
#     bot.send_message(message.chat.id, message.text)

@bot.message_handler(content_types=['text'])
def handle_text(message):
    text = message.text.lower()
    if text == 'погода на завтра':
        bot.send_chat_action(chat_id=message.chat.id, action='typing')  # анимация "Печатает..."
        bot.send_message(message.chat.id, weather_api.show_tomorrow_weather())
    elif text == 'погода сейчас':
        bot.send_chat_action(chat_id=message.chat.id, action='typing')
        bot.send_message(message.chat.id, weather_api.show_current_weather())
    elif text == 'как дела?':
        bot.send_message(message.chat.id, 'Отлично. А твои как?')
    elif text == 'помощь':
        bot.send_message(message.chat.id, 'Пока в разработке...')
    elif text == 'настройка бота':
        bot.send_message(message.chat.id, 'Пока в разработке...')
    elif text == 'подписаться на уведомления':
        # проверить если пользователь в базе данных, если нет, то добавить
        if check_in_db(column='user_id', data_check=message.chat.id):
            subscribe(message)
        else:
            add_user_in_db(user_name=message.chat.username, user_id=message.chat.id)
            subscribe(message)
    elif text == 'отписаться':
        if check_in_db(column='user_id', data_check=message.chat.id):
            unsubscribe(message)
        else:
            bot.send_message(message.chat.id, 'Вы еще не подписывались на уведомления!')
    elif text == 'ошибка' or text == '/help' or text == 'возникла ошибка':
        keyboard = telebot.types.InlineKeyboardMarkup()
        keyboard.add(telebot.types.InlineKeyboardButton('Написать разаботчику', url='telegram.me/serbul_evhenii'))
        bot.send_message(message.chat.id,
                         f"Если возникла ошибка или Вы нашли баг в боте, сообщите пожалуйста разработчику.",
                         reply_markup=keyboard)
    else:
        pass
        # bot.send_message(message.chat.id, message.text)


@bot.message_handler(content_types=['photo'])
def text_handler(message):
    bot.send_message(message.chat.id, 'Вау, красиво!')


if __name__ == '__main__':
    init_db()
    bot.polling(none_stop=True)
