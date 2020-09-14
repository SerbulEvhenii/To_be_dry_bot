import os
import requests
import json
import emoji
import datetime

API_KEY = 'a4d2b023b22c75b54f2b88fb96430925'
USER_LATITUDE = 50.479211
USER_LONGITUDE = 30.434911
URL_WEATHER = f'https://api.openweathermap.org/data/2.5/onecall?lat={USER_LATITUDE}&lon={USER_LONGITUDE}' \
              f'&exclude=minutely,hourly,&appid={API_KEY}&lang=ru&units=metric'


def get_weather():
    date_now = datetime.datetime.now()
    if not os.path.exists('weather.json'):  # если файл отсутствует, то нужно его создать
        save_json()
    last_save_file = datetime.datetime.fromtimestamp(os.path.getmtime('weather.json')) + datetime.timedelta(minutes=10)
    if os.path.exists('weather.json'):
        if last_save_file > date_now:  # если после сохранения прошло < 10мин, прочти файл
            return read_json()
        if last_save_file < date_now:  # если после сохранения прошло > 10мин, сохрани заново, и прочти файл
            save_json()
            return read_json()


def show_current_weather():
    temp = round((get_weather())['current']['temp'], 0)
    return f'Сейчас в Киеве температура воздуха: {temp}.'


def show_current_daily_weather():
    temp_min = round((get_weather())['daily'][0]['temp']['min'], 0)  # [0] - сегодня, 1 - завтра
    temp_max = round((get_weather())['daily'][0]['temp']['max'], 0)  # [0] - сегодня, 1 - завтра
    pop = int((get_weather())['daily'][0]['pop']) * 100  # Вероятность осадков % (Precipitation)
    return emoji.emojize(f'Погода на сегодня в Киеве:\n'
                         f'• :sun_behind_cloud: температура воздуха:\n'
                         f'мин. +{temp_min} макс. +{temp_max}\n'
                         f'• :cloud_with_rain: вероятность осадков: {pop}%')


def show_tomorrow_weather():
    temp_min = round((get_weather())['daily'][1]['temp']['min'], 0)  # [1] - сегодня, 2 - завтра
    temp_max = round((get_weather())['daily'][1]['temp']['max'], 0)  # [1] - сегодня, 2 - завтра
    pop = int((get_weather())['daily'][1]['pop']) * 100  # Вероятность осадков % (Precipitation)
    return emoji.emojize(f'Погода на завтра в Киеве:\n'
                         f'• :sun_behind_cloud: температура воздуха:\n'
                         f'мин. +{temp_min} макс. +{temp_max}\n'
                         f'• :cloud_with_rain: вероятность осадков: {pop}%')


def save_json(filename='weather.json'):
    r = requests.get(URL_WEATHER)
    r_json = r.json()
    with open(filename, 'w') as f:
        json.dump(r_json, f, indent=2, ensure_ascii=False)


def read_json():
    with open('weather.json', 'r') as f:
        return json.load(f)


if __name__ == '__main__':
    pass
