import telebot
from config import TOKEN # подключаем конфиг, чтобы взять с него токен бота

bot = telebot.TeleBot(TOKEN)
print('Бот запущен...')
# print(bot.get_me())
