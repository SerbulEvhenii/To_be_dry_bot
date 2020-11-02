# файл отвечает за разметку кнопок меню
import telebot
import emoji # Импортируем смайлы http://www.unicode.org/emoji/charts/full-emoji-list.html

markup_main = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
markup_main_btn_settings_bot = telebot.types.KeyboardButton(emoji.emojize(':gear: Настройка бота'))
markup_main_btn_weather_current = telebot.types.KeyboardButton(emoji.emojize(':sun_behind_small_cloud: Погода сегодня'))
markup_main_btn_weather_tomorrow = telebot.types.KeyboardButton(emoji.emojize(':sun_behind_small_cloud: Погода на завтра'))
markup_main_btn_subscribe = telebot.types.KeyboardButton(emoji.emojize(':bell: Подписаться'))
markup_main_btn_unsubscribe = telebot.types.KeyboardButton(emoji.emojize(':bell_with_slash: Отписаться'))
markup_main_btn_help = telebot.types.KeyboardButton(emoji.emojize(':construction: Помощь'))
markup_main_btn_error = telebot.types.KeyboardButton(emoji.emojize(':warning: Возникла ошибка'))
markup_main.row(markup_main_btn_settings_bot)
markup_main.row(markup_main_btn_weather_current, markup_main_btn_weather_tomorrow)
markup_main.row(markup_main_btn_subscribe, markup_main_btn_unsubscribe)
markup_main.row(markup_main_btn_help, markup_main_btn_error)
