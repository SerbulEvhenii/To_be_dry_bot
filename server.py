import json
import os
from flask import Flask, request, abort, jsonify
import telebot
from config import TOKEN

# TZ Europe/Kiev
URL = 'https://testserbulbot.herokuapp.com/'


bot = telebot.TeleBot(TOKEN)  # Создание бота
app = Flask(__name__)      # Создание сервера

# def write_json(data, filename='answer.json'):
#     with open(filename, 'w') as f:
#         json.dump(data, f, indent=2, ensure_ascii=False)


@app.route('/', methods=['GET', 'HEAD'])
def index():
    return ''


@app.route('/' + TOKEN, methods=['POST'])
def telegram_webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        abort(403)


# @app.route('/')
# def webhook():
#     bot.set_webhook(url='https://testserbulbot.herokuapp.com/' + TOKEN)
#     return "!", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))