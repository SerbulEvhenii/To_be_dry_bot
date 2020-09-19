# import telebot
import config  # подключаем конфиг, чтобы взять с него токен бота
#
# bot = telebot.TeleBot(config.TOKEN)
# print('Бот запущен...')
# # print(bot.get_me())

#worker: python bot_handlers.py

import telebot
import os
from flask import Flask, request
import logging

bot = telebot.TeleBot(config.TOKEN)
print('Бот запущен...')
# Здесь пишем наши хэндлеры

# Проверим, есть ли переменная окружения Хероку (как ее добавить смотрите ниже)
# if "HEROKU" in list(os.environ.keys()):
#     logger = telebot.logger
#     telebot.logger.setLevel(logging.INFO)
#
#     server = Flask(__name__)
#     @server.route("/bot", methods=['POST'])
#     def getMessage():
#         bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
#         return "!", 200
#     @server.route("/")
#     def webhook():
#         bot.remove_webhook()
#         bot.set_webhook(url="https://bot-to-be-dry.herokuapp.com/") # этот url нужно заменить на url вашего Хероку приложения
#         return "?", 200
#     server.run(host="0.0.0.0", port=os.environ.get('PORT', 80))
# else:
#     # если переменной окружения HEROKU нету, значит это запуск с машины разработчика.
#     # Удаляем вебхук на всякий случай, и запускаем с обычным поллингом.
#     bot.remove_webhook()
#     bot.polling(none_stop=True)