import telebot

markup_main = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
markup_main_btn_settings_bot = telebot.types.KeyboardButton('Настройка бота')
markup_main_btn_weather_current = telebot.types.KeyboardButton('Погода сейчас')
markup_main_btn_weather_tomorrow = telebot.types.KeyboardButton('Погода на завтра')
markup_main_btn_subscribe = telebot.types.KeyboardButton('Подписаться на уведомления')
markup_main_btn_unsubscribe = telebot.types.KeyboardButton('Отписаться')
markup_main_btn_help = telebot.types.KeyboardButton('Помощь')
markup_main_btn_error = telebot.types.KeyboardButton('Возникла ошибка')
markup_main.row(markup_main_btn_settings_bot)
markup_main.row(markup_main_btn_weather_current, markup_main_btn_weather_tomorrow)
markup_main.row(markup_main_btn_subscribe, markup_main_btn_unsubscribe)
markup_main.row(markup_main_btn_help, markup_main_btn_error)
