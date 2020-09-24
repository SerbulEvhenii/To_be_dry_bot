from flask import Flask, request
import telebot
from config import TOKEN, URL, bot_user_name

# start the flask app
app = Flask(__name__)


