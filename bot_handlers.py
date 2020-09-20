import datetime
import os
import threading
import db
from bot_config import bot
from db import *  # Импортируем все методы из файла для базы данных
import weather_api  # Импортируем все методы из файла для погоды
import telebot.types  # Импортируем типы телеграма API
import markups  # Импортируем кнопки для бота
import inlineKeyboard  # Импортируем инлайн кавиатуры
import emoji  # Импортируем смайлы http://www.unicode.org/emoji/charts/full-emoji-list.html
import time
import schedule


@bot.message_handler(commands=['start'])
# Выполняется, когда пользователь вызывает /start
def send_welcome(message):
    if check_in_db(column='user_id', data_check=message.chat.id):
        bot.send_message(message.chat.id, f'Снова привет, {message.chat.first_name}!',
                         reply_markup=markups.markup_main)
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
        bot.send_message(message.chat.id, 'Вы уже подписаны на уведомления.')
    else:
        subscribe_db(user_id=message.chat.id)
        bot.send_message(message.chat.id, 'Вы успешно подписались на уведомления. По умолчанию я показываю '
                                          'погоду для города Киева.')


@bot.message_handler(commands=['unsubs'])
# Выполняется, когда пользователь вызывает /unsubs
def unsubscribe(message):
    unsubscribe_db(user_id=message.chat.id)
    bot.send_message(message.chat.id, 'Вы успешно отписались от уведомлений.')

# @bot.message_handler(content_types=['text'])
# # Выполняется, когда пользователь вызывает /unsubs
# def test_set_text(message):
#     text = message.text.lower()
#     if 'тест' in text:
#         print(message.text)
#         bot.send_message(message.chat.id, 'Тестируем получение текста из сообщения')


# @bot.message_handler(commands=['time'])
# # Выполняется, когда пользователь вызывает /time
# def set_time_notify_in_db(message):
#     set_time_notify(user_id=message.chat.id, time='07:00')
#     bot.send_message(message.chat.id, SET_TIME_NOTIFY)

def notify_weather():
    time_now = datetime.datetime.now().strftime('%H:%M')
    list_tuples_id_users = db.list_id_users_in_db()
    list_id_users = []
    for tuple_in_list in list_tuples_id_users:
        list_id_users.append(tuple_in_list[1])
    for user_id_in_list in list_id_users:
        if db.get_time_notify_user_db(user_id=user_id_in_list) == time_now:
            bot.send_message(chat_id=user_id_in_list, text=weather_api.show_current_daily_weather())


# Выполняется, когда пользователь вызывает /time
def set_time_notify_in_db(callback_query, time):
    time_notify = time
    set_time_notify(user_id=callback_query.from_user.id, time=time_notify)

def set_time_notify_in_db_text_message_user(user_id, time):
    time_notify = time
    set_time_notify(user_id=user_id, time=time_notify)


# Отображение 2х кнопок "Настройки бота": настройка времени и настройка местоположения
def start_menu_settings(message):
    bot.send_message(message.chat.id, 'Настройки бота:', reply_markup=inlineKeyboard.inline_kb_settings)


# Отображения времени выбора
def start_menu_all_times(callback_query):
    bot.send_message(callback_query.from_user.id, 'Выберите подходящее для Вас время, для ведомлений.',
                     reply_markup=inlineKeyboard.inline_kb_all_times)


# Реакция нажатия на кнопки из меню: "Настройки бота"
@bot.callback_query_handler(func=lambda c: c.data and c.data.startswith('menu'))
def set_time_notify_menu(callback_query: telebot.types.CallbackQuery):
    if callback_query.data == 'menu_btn_geo':
        bot.answer_callback_query(callback_query.id)
        bot.send_message(callback_query.from_user.id, 'Передача местоположения в разработке')
    elif callback_query.data == 'menu_btn_notify':
        bot.answer_callback_query(callback_query.id)
        start_menu_all_times(callback_query)


# Реакция кнопок со временем уведомлений
@bot.callback_query_handler(func=lambda c: c.data and c.data.startswith('btn'))
def set_time_notify_menu(callback_query: telebot.types.CallbackQuery):
    if callback_query.data == 'btn_edit':
        msg = bot.send_message(callback_query.from_user.id,
                               'Введите время на которое вы хотите поставить уведомление? Например: 07:00')
        bot.register_next_step_handler(msg, time_user)
    else:
        for time in inlineKeyboard.btn_tuple_data:
            if callback_query.data == time:
                bot.answer_callback_query(callback_query.id)
                set_time_notify(user_id=callback_query.from_user.id, time=callback_query.data[3:])
                bot.send_message(callback_query.from_user.id, f'Время уведомления установлено на {callback_query.data[3:]}')



# @bot.callback_query_handler(func=lambda c: c.data == '07:00')
# def process_callback_btn(callback_query: telebot.types.CallbackQuery):
#     bot.answer_callback_query(callback_query.id)
#     bot.send_message(callback_query.from_user.id, 'Нажата 07:00')


# @bot.message_handler(content_types=["text"])  # Любой текст
# def repeat_all_messages(message):
#     bot.send_message(message.chat.id, message.text)

def time_user(message):
    id = message.chat.id
    text = message.text
    set_time_notify_in_db_text_message_user(id, text)
    bot.send_message(id, f'Время уведомления установлено на {text}.')

@bot.message_handler(content_types=['text'])
def handle_text(message):
    text = message.text.lower()
    if 'погода на завтра' in text:
        bot.send_chat_action(chat_id=message.chat.id, action='typing')  # анимация "Печатает..."
        bot.send_message(message.chat.id, weather_api.show_tomorrow_weather())
    elif 'погода сейчас' in text:
        bot.send_chat_action(chat_id=message.chat.id, action='typing')
        bot.send_message(message.chat.id, weather_api.show_current_weather())
    elif 'погода сегодня' in text:
        bot.send_chat_action(chat_id=message.chat.id, action='typing')
        bot.send_message(message.chat.id, weather_api.show_current_daily_weather())
    elif 'выбор времени уведомлений' in text:
        msg = bot.send_message(message.chat.id, 'Введите время на которое вы хотите поставить уведомление? Например: 07:00')
        bot.register_next_step_handler(msg, time_user)
    #     bot.send_message(message.chat.id, 'Введите время на которое вы хотите поставить уведомление? Например: 07:00')
    #     msg = bot.reply_to(message, 'Введите время на которое вы хотите поставить уведомление? Например: 07:00')
    #     bot.register_next_step_handler(msg, set_time_notify_in_db_text_message(time=message.text))
    #     set_time_notify_in_db_text_message(message_2.chat.id, time=message_2.text)
    elif 'как дела?' in text:
        bot.send_message(message.chat.id, 'Отлично. А твои как?')
    elif 'помощь' in text:
        bot.send_message(message.chat.id, 'Пока в разработке...')
    elif 'настройка бота' in text:
        start_menu_settings(message)
    elif 'подписаться' in text:
        # проверить если пользователь в базе данных, если нет, то добавить
        if check_in_db(column='user_id', data_check=message.chat.id):
            subscribe(message)
        else:
            add_user_in_db(user_name=message.chat.username, user_id=message.chat.id)
            subscribe(message)
    elif 'отписаться' in text:
        if check_in_db(column='user_id', data_check=message.chat.id):
            unsubscribe(message)
        else:
            bot.send_message(message.chat.id, 'Вы еще не подписывались на уведомления!')
    elif 'ошибка' in text or '/help' in text or 'help' in text or 'возникла ошибка' in text:
        keyboard = telebot.types.InlineKeyboardMarkup()
        keyboard.add(telebot.types.InlineKeyboardButton(emoji.emojize(':pencil: Написать разаботчику'),
                                                        url='telegram.me/serbul_evhenii'))
        bot.send_message(message.chat.id,
                         f"Если возникла ошибка или Вы нашли баг в боте, сообщите пожалуйста разработчику.",
                         reply_markup=keyboard)
    else:
        pass
        # bot.send_message(message.chat.id, message.text)


@bot.message_handler(content_types=['photo'])
def text_handler(message):
    bot.send_message(message.chat.id, 'Вау, красиво!')


def runBot():  # инициализация БД и запуск бота
    init_db()
    bot.polling(none_stop=True)

# def runBotServerFlask():  # инициализация БД и запуск бота на сервере Flask
#     init_db()
#     server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 443)))


# def runSchedulers():  # запус расписания
#     schedule.every().day.at("05:00").do(notify_weather)
#     schedule.every().day.at("06:00").do(notify_weather)
#     schedule.every().day.at("07:00").do(notify_weather)
#     schedule.every().day.at("08:00").do(notify_weather)
#     schedule.every().day.at("09:00").do(notify_weather)
#     schedule.every().day.at("10:00").do(notify_weather)
#     schedule.every().day.at("11:00").do(notify_weather)
#     schedule.every().day.at("12:00").do(notify_weather)
#     schedule.every().day.at("13:00").do(notify_weather)
#     schedule.every().day.at("14:00").do(notify_weather)
#     schedule.every().day.at("15:00").do(schedule_bot.notify_weather_15_00)
#     schedule.every().day.at("16:00").do(notify_weather)
#     schedule.every().day.at("17:00").do(notify_weather)
#     schedule.every().day.at("18:00").do(notify_weather)
#     schedule.every().day.at("19:00").do(notify_weather)
#     schedule.every().day.at("20:00").do(notify_weather)
#     schedule.every().day.at("21:00").do(notify_weather)
#     schedule.every().day.at("22:00").do(notify_weather)
#     schedule.every().day.at("23:00").do(notify_weather)
#     while True:
#         schedule.run_pending()
#         time.sleep(1)


if __name__ == '__main__':
    runBot()
    # t1 = threading.Thread(target=runBotServerFlask)
    # t2 = threading.Thread(target=runSchedulers)
    # t1.start()
    # t2.start()

