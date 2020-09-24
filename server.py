import os
from flask import Flask, request, abort
import telebot
from config import TOKEN

# TZ Europe/Kiev


bot = telebot.TeleBot(TOKEN)  # Создание бота
app = Flask(__name__)      # Создание сервера


@app.route('/' + 'bot' + TOKEN, methods=['POST'])
# def getMessage():
#     bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
#     return "!", 200
def telegram_webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.stream.read().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return 'ok', 200
    else:
        abort(403)


@app.route('/')
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://testserbulbot.herokuapp.com/' + TOKEN)
    return "!", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))