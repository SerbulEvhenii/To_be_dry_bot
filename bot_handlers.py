import datetime
import threading
import os
import bot_schedule
import db_postgreSQL as db  # Импортируем все методы из файла для базы данных
import weather_api  # Импортируем все методы из файла для погоды
import telebot.types  # Импортируем типы телеграма API
import markups  # Импортируем кнопки для бота
import inlineKeyboard  # Импортируем инлайн кавиатуры
import emoji  # Импортируем смайлы http://www.unicode.org/emoji/charts/full-emoji-list.html
from flask import Flask, request, abort, jsonify, Response
from telebot import types, TeleBot
import config


URL = 'https://bot-to-be-dry.herokuapp.com/'
bot = TeleBot(config.TOKEN, threaded=False)         # Создание бота
app = Flask(__name__)                               # Создание сервера


@app.route('/')
def index():
    return '<h1>Telegram BOT - To be dry. Погодный бот by Serbul Evhenii</h1>', 200

@app.route("/wakemydyno.txt")    # http://wakemydyno.com/ - не даем заснуть dyno
def get_text():
    content = 'Test ping Heroku'
    return Response(content, mimetype="text/plain")


@app.route('/' + config.TOKEN, methods=["POST"])
def webhook():
    bot.process_new_updates([types.Update.de_json(request.stream.read().decode("utf-8"))])
    # json_string = request.stream.read().decode('utf-8')
    # update = types.Update.de_json(json.load(json_string), bot)
    # bot.process_new_updates(update)
    return "ok", 200


@bot.message_handler(commands=['start'])
# Выполняется, когда пользователь вызывает /start
def send_welcome(message):
    if db.check_in_db(column='user_id', data_check=message.chat.id):
        bot.send_message(message.chat.id, f'Снова привет, {message.chat.first_name} 🤚🏼',
                         reply_markup=markups.markup_main)
    else:
        db.add_user_in_db(user_name=message.chat.username, user_id=message.chat.id)
        bot.send_message(message.chat.id,
                         f'Привет, {message.chat.first_name} 🤚🏼\n'
                         f'Я погодный Бот! Я буду оповещать тебя, если в ближайшее время в твоем городе будет идти '
                         f'дождь.', reply_markup=markups.markup_main)


@bot.message_handler(commands=['subs'])
# Выполняется, когда пользователь вызывает /subs
def subscribe(message):
    if db.check_subscribe_db(user_id=message.chat.id):
        bot.send_message(message.chat.id, 'Вы уже подписаны на уведомления.')
    else:
        db.subscribe_db(user_id=message.chat.id)
        bot.send_message(message.chat.id, 'Вы успешно подписались на уведомления. По умолчанию я показываю '
                                          'погоду для города Киева. В настройках бота Вы можете сменить город.')


@bot.message_handler(commands=['unsubs'])
# Выполняется, когда пользователь вызывает /unsubs
def unsubscribe(message):
    db.unsubscribe_db(user_id=message.chat.id)
    bot.send_message(message.chat.id, 'Вы успешно отписались от уведомлений.')


@bot.message_handler(commands=['users'])
# Выполняется, когда пользователь вызывает /users
def admin_count_users(message):
    users = db.count_users()
    bot.send_message(message.chat.id, f'Колличество зарегистрированных пользователей бота: {users}')


def notify_weather():
    time_now = datetime.datetime.now().strftime('%H:%M')
    list_tuples_id_users = db.list_id_users_in_db()
    list_id_users = []
    for tuple_in_list in list_tuples_id_users:
        list_id_users.append(tuple_in_list[1])
    for user_id_in_list in list_id_users:
        if db.get_time_notify_user_db(user_id=user_id_in_list) == time_now and db.check_subscribe_db(user_id=user_id_in_list):
            bot.send_message(chat_id=user_id_in_list, text=weather_api.show_current_daily_weather(user_id_in_list))


# Выполняется, когда пользователь вызывает /time
def set_time_notify_in_db(callback_query, time):
    time_notify = time
    db.set_time_notify(user_id=callback_query.from_user.id, time=time_notify)


def set_time_notify_in_db_text_message_user(user_id, time):
    time_notify = time
    db.set_time_notify(user_id=user_id, time=time_notify)


# Отображение 2х кнопок "Настройки бота": настройка времени и настройка местоположения
def start_menu_settings(message):
    bot.send_message(message.chat.id, 'Настройки бота:', reply_markup=inlineKeyboard.inline_kb_settings)


# Отображения времени выбора
def start_menu_all_times(callback_query):
    bot.send_message(callback_query.from_user.id, 'Выберите подходящее для Вас время, для уведомлений.',
                     reply_markup=inlineKeyboard.inline_kb_all_times)


# # Реакция нажатия на кнопки из меню: "Настройки бота"
# @bot.callback_query_handler(func=lambda c: c.data and c.data.startswith('menu'))
# def set_time_notify_menu(callback_query: telebot.types.CallbackQuery):
#     if callback_query.data == 'menu_btn_geo':
#         bot.answer_callback_query(callback_query.id)
#         bot.send_message(callback_query.from_user.id, 'Передача местоположения в разработке')
#     elif callback_query.data == 'menu_btn_notify':
#         bot.answer_callback_query(callback_query.id)
#         start_menu_all_times(callback_query)


# Реакция нажатия на кнопки из меню: "Настройки бота"
@bot.callback_query_handler(func=lambda c: c.data and c.data.startswith('menu'))
def set_time_notify_menu(callback_query: telebot.types.CallbackQuery):
    if callback_query.data == 'menu_btn_geo':
        bot.answer_callback_query(callback_query.id)
        bot.send_message(callback_query.from_user.id, 'Настройка местоположения:')
        get_geo_position(callback_query)
    elif callback_query.data == 'menu_btn_notify':
        bot.answer_callback_query(callback_query.id)
        start_menu_all_times(callback_query)


def get_geo_position(callback_query):
    city = weather_api.get_geo_city(callback_query.from_user.id)
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_geo = types.KeyboardButton(text=emoji.emojize(":compass: Отправить местоположение"), request_location=True)
    button_main_menu = types.KeyboardButton(text=emoji.emojize(":gear: Главное меню"))
    keyboard.add(button_geo, button_main_menu)
    bot.send_message(callback_query.from_user.id, emoji.emojize(f":house: Ваше местоположение определено как: {city}.\n"
                                                  f"⁉ Чтобы я мог запомнить для какого города "
                                                  f"показывать тебе погоду, передай мне пожалуйста свое местоположение "
                                                  f"один раз и я запомню. Перед тем как нажать кнопку ниже "
                                                  f"'Отправить местоположение' включи в настройках своего телефона "
                                                  f"GPS (местоположение)."),
                                                  reply_markup=keyboard)


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
                db.set_time_notify(user_id=callback_query.from_user.id, time=callback_query.data[3:])
                bot.send_message(callback_query.from_user.id, f'Время уведомления установлено на {callback_query.data[3:]}')


def time_user(message):
    id = message.chat.id
    text = message.text
    set_time_notify_in_db_text_message_user(id, text)
    bot.send_message(id, f'Время уведомления установлено на {text}.')


@bot.message_handler(content_types=["location"])
def location(message):
    if message.location is not None:
        bot.send_message(message.chat.id, "Отлично! Я запомнил в каком городе ты находишься. Теперь я буду показывать "
                                          "погоду для твоего города.",
                                          reply_markup=markups.markup_main)
        db.set_geoposition(user_id=message.chat.id, latit=message.location.latitude, long=message.location.longitude)


@bot.message_handler(content_types=['text'])
def handle_text(message):
    text = message.text.lower()
    if 'погода на завтра' in text:
        bot.send_chat_action(chat_id=message.chat.id, action='typing')  # анимация "Печатает..."
        bot.send_message(message.chat.id, weather_api.show_tomorrow_weather(message.chat.id))
    elif 'погода сейчас' in text:
        bot.send_chat_action(chat_id=message.chat.id, action='typing')
        bot.send_message(message.chat.id, weather_api.show_current_weather(message.chat.id))
        db.get_geoposition(user_id=message.chat.id)
    elif 'погода сегодня' in text:
        bot.send_chat_action(chat_id=message.chat.id, action='typing')
        bot.send_message(message.chat.id, weather_api.show_current_daily_weather(message.chat.id))
    elif 'главное меню' in text:
        bot.send_message(message.chat.id, 'Главное меню', reply_markup=markups.markup_main)
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
        if db.check_in_db(column='user_id', data_check=message.chat.id):
            subscribe(message)
        else:
            db.add_user_in_db(user_name=message.chat.username, user_id=message.chat.id)
            subscribe(message)
    elif 'отписаться' in text:
        if db.check_in_db(column='user_id', data_check=message.chat.id):
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


@bot.message_handler(content_types=['photo'])
def text_handler(message):
    bot.send_message(message.chat.id, 'Вау, красиво!')


def runBotServerFlask():  # инициализация БД и запуск бота на сервере Flask
    print('База данных инициализированна...')
    db.init_db()
    print('Сервер запущен...')
    bot.set_webhook(url=URL + config.TOKEN)
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))

#
# def runSchedulers():
#     print('Расписание запущено...')
#     while True:
#         schedule.run_pending()
#         time.sleep(1)

def runBotHome():
    bot.remove_webhook()
    db.init_db()
    print('База данных инициализированна...')
    print('Бот запущен...')
    bot.polling(none_stop=True)

def runSchedulers():
    bot_schedule.start_schedule()



# дом
# if __name__ == '__main__':
#     t1 = threading.Thread(target=runBotHome)
#     t2 = threading.Thread(target=runSchedulers)
#     t1.start()
#     t2.start()

# if __name__ == "__main__":
#     db.init_db()
#     print('База данных инициализированна...')
#     app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))

# Heroku
if __name__ == '__main__':
    t1 = threading.Thread(target=runBotServerFlask)
    t2 = threading.Thread(target=runSchedulers)
    t1.start()
    t2.start()


