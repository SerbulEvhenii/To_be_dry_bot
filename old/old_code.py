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



# https://api.telegram.org/bot1179933255:AAHDd5ZeR9FgnVEp02sVwHyUIuKU34VNZsk/getWebhookInfo

# https://api.telegram.org/bot1179933255:AAHDd5ZeR9FgnVEp02sVwHyUIuKU34VNZsk/deleteWebhook

# https://api.telegram.org/bot1179933255:AAHDd5ZeR9FgnVEp02sVwHyUIuKU34VNZsk/setWebhook?url=https://bot-to-be-dry.herokuapp.com/1179933255:AAHDd5ZeR9FgnVEp02sVwHyUIuKU34VNZsk