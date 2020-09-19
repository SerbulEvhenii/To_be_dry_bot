# import telebot
# import config  # подключаем конфиг, чтобы взять с него токен бота
#
# bot = telebot.TeleBot(config.TOKEN)
# print('Бот запущен...')
# # print(bot.get_me())



from flask import Flask, request
import telebot
from config import TOKEN as TOKEN

bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)


@server.route('/' + TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://bot-to-be-dry.herokuapp.com/' + TOKEN)
    return "!", 200

