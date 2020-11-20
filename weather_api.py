# в этом файле описана вся логика работы с API погоды
import os
import requests
import json
import emoji
import datetime
import db_postgreSQL as db

API_KEY = os.environ['API_WEATHER']
USER_LATITUDE = 50.479211
USER_LONGITUDE = 30.434911
URL_WEATHER = f'https://api.openweathermap.org/data/2.5/onecall?lat={USER_LATITUDE}&lon={USER_LONGITUDE}' \
              f'&exclude=minutely,hourly,&appid={API_KEY}&lang=ru&units=metric'


def get_URL_WEATHER(user_id: int) -> str:  # принимает id пользователя, возвращает URL запрос для этого города
    user_latitude, user_longitude = db.get_geoposition(user_id=user_id)
    URL_WEATHER = f'https://api.openweathermap.org/data/2.5/onecall?lat={user_latitude}&lon={user_longitude}' \
                  f'&exclude=minutely,hourly,&appid={API_KEY}&lang=ru&units=metric'
    return URL_WEATHER


def get_weather(user_id: int):
    save_json(user_id)
    return read_json()


def show_current_weather(user_id: int) -> str:  # принимает id пользователя и возвращает погоду на данный момент в городе
    temp = round((get_weather(user_id))['current']['temp'], 0)
    return f'Сейчас в Киеве температура воздуха: {temp}.'


def show_current_daily_weather(user_id: int) -> str:  # принимает id пользователя и возвращает прогноз погоды на сегодня (весь день)
    get_weather(user_id)
    city = db.get_city_user_db(user_id=user_id)
    temp_min = round((read_json())['daily'][0]['temp']['min'], 0)  # [0] - сегодня, 1 - завтра
    temp_max = round((read_json())['daily'][0]['temp']['max'], 0)  # [0] - сегодня, 1 - завтра
    feel_temp_morn = round((read_json())['daily'][0]['feels_like']['morn'], 0)
    feel_temp_day = round((read_json())['daily'][0]['feels_like']['day'], 0)
    feel_temp_eve = round((read_json())['daily'][0]['feels_like']['eve'], 0)
    pop = int((read_json())['daily'][0]['pop'] * 100)  # Вероятность осадков % (Precipitation)
    date_api = datetime.datetime.fromtimestamp((read_json())['daily'][0]['dt'])
    date_api_str = date_api.strftime('%d.%m')
    return emoji.emojize(f'Погода на сегодня ({date_api_str}):\n'
                         f':world_map: {city}\n'
                         f':sun_behind_cloud: температура воздуха:\n'
                         f'• мин. {temp_min} макс. {temp_max}\n'
                         f'Ощущается:\n'
                         f'• утром {feel_temp_morn}\n'
                         f'• в обед {feel_temp_day}\n'
                         f'• вечером {feel_temp_eve}\n'
                         f':cloud_with_rain: вероятность осадков: {pop}%')


def show_tomorrow_weather(user_id: int) -> str:  # принимает id пользователя и возвращает прогноз погоды на завтра
    city = db.get_city_user_db(user_id=user_id)
    temp_min = round((read_json())['daily'][1]['temp']['min'], 0)  # [1] - сегодня, 2 - завтра
    temp_max = round((read_json())['daily'][1]['temp']['max'], 0)  # [1] - сегодня, 2 - завтра
    pop = int((read_json())['daily'][1]['pop'] * 100)  # Вероятность осадков % (Precipitation)
    date_api = datetime.datetime.fromtimestamp((read_json())['daily'][1]['dt'])
    date_api_str = date_api.strftime('%d.%m')
    return emoji.emojize(f'Погода на завтра ({date_api_str}):\n'
                         f':world_map: {city}\n'
                         f'• :sun_behind_cloud: температура воздуха:\n'
                         f'мин. {temp_min} макс. {temp_max}\n'
                         f'• :cloud_with_rain: вероятность осадков: {pop}%')


def save_json(user_id: int, filename='weather.json'):  # принимает id пользователя и сохраняет json файл с погодой
    url_weather_user = get_URL_WEATHER(user_id)
    r = requests.get(url_weather_user)
    r_json = r.json()
    with open(filename, 'w') as f:
        json.dump(r_json, f, indent=2, ensure_ascii=False)


def read_json():  # открывает и читает данные из файла с погодой
    with open('weather.json', 'r') as f:
        return json.load(f)
