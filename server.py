import os
from flask import Flask, request
import telebot
from config import TOKEN

# TZ Europe/Kiev


bot = telebot.TeleBot(TOKEN)  # Создание бота
server = Flask(__name__)      # Создание сервера


@server.route('/' + TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


@server.route('/')
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://testserbulbot.herokuapp.com/' + TOKEN)
    return "!", 200


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))