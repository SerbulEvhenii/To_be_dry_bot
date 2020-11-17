# ПРОВЕРКА ПОГОДЫ С ПРОВЕРКОЙ 10МИН
# def get_weather():
#     date_now = datetime.datetime.now()
#     if not os.path.exists('weather.json'):  # если файл отсутствует, то нужно его создать
#         save_json()
#     last_save_file = datetime.datetime.fromtimestamp(os.path.getmtime('weather.json')) + datetime.timedelta(minutes=10)
#     if os.path.exists('weather.json'):
#         if last_save_file > date_now:  # если после сохранения прошло < 10мин, прочти файл
#             return read_json()
#         if last_save_file < date_now:  # если после сохранения прошло > 10мин, сохрани заново, и прочти файл
#             save_json()
#             return read_json()



# # Реакция нажатия на кнопки из меню: "Настройки бота"
# @bot.callback_query_handler(func=lambda c: c.data and c.data.startswith('menu'))
# def set_time_notify_menu(callback_query: telebot.types.CallbackQuery):
#     if callback_query.data == 'menu_btn_geo':
#         bot.answer_callback_query(callback_query.id)
#         bot.send_message(callback_query.from_user.id, 'Настройка местоположения:')
#         get_geo_position(callback_query)
#     elif callback_query.data == 'menu_btn_notify':
#         bot.answer_callback_query(callback_query.id)
#         start_menu_all_times(callback_query)








# def runBotHome():
#     bot.remove_webhook()
#     db.init_db()
#     print('База данных инициализированна...')
#     print('Бот запущен...')
#     bot.polling(none_stop=True)




# https://api.telegram.org/bot1179933255:AAHDd5ZeR9FgnVEp02sVwHyUIuKU34VNZsk/getWebhookInfo

# https://api.telegram.org/bot1179933255:AAHDd5ZeR9FgnVEp02sVwHyUIuKU34VNZsk/deleteWebhook

# https://api.telegram.org/bot1179933255:AAHDd5ZeR9FgnVEp02sVwHyUIuKU34VNZsk/setWebhook?url=https://bot-to-be-dry.herokuapp.com/1179933255:AAHDd5ZeR9FgnVEp02sVwHyUIuKU34VNZsk