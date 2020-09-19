# import telebot
# import config  # подключаем конфиг, чтобы взять с него токен бота
#
# bot = telebot.TeleBot(config.TOKEN)
# print('Бот запущен...')
# # print(bot.get_me())
import os

import flask
import telebot
from config import TOKEN as TOKEN

bot = telebot.TeleBot(TOKEN)
server = flask.Flask(__name__)


@server.route('/' + TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(flask.request.stream.read().decode("utf-8"))])
    return "!", 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://bot-to-be-dry.herokuapp.com/' + TOKEN)
    return "!", 200

server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))