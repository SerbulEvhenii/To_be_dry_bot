import json
import os
from flask import Flask, request, abort, jsonify
from telebot import types, TeleBot
from config import TOKEN

# TZ Europe/Kiev
URL = 'https://testserbulbot.herokuapp.com/'


bot = TeleBot(TOKEN, threaded=False)  # Создание бота
app = Flask(__name__)      # Создание сервера

@app.route('/' + TOKEN, methods=["POST"])
def webhook():
    bot.process_new_updates([types.Update.de_json(request.stream.read().decode("utf-8"))])
    print("Message")
    return "ok", 200


@bot.message_handler(commands=['start', 'help'])
def startCommand(message):
    bot.send_message(message.chat.id, 'Hi *' + message.chat.first_name + '*!')



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))