import telebot

TOKEN = '1177989498:AAFm8PVPsdSk_ybHQzSI7rSifwQIUSRzD5A'

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Howdy, how are you doing?")
	print(message)


@bot.message_handler(commands=['login'])
def login(message):
	bot.reply_to(message, "Howdy, how are you doing?")
	print(message)
	print(message.text)


@bot.message_handler(func=lambda message: True)
def echo_all(message):
	bot.reply_to(message, message.text)

if __name__ == '__main__':

    bot.polling()