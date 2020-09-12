import requests
import json

API_KEY = 'a4d2b023b22c75b54f2b88fb96430925'
USER_LATITUDE = 50.479211
USER_LONGITUDE = 30.434911
URL_WEATHER = f'https://api.openweathermap.org/data/2.5/onecall?lat={USER_LATITUDE}&lon={USER_LONGITUDE}' \
              f'&exclude=minutely,hourly,&appid={API_KEY}&lang=ru&units=metric'

def save_weather_json():
    r = requests.get(URL_WEATHER)
    r_json = r.json()
    write_json(r_json)


def get_weather():
    r = requests.get(URL_WEATHER)
    r_json = r.json()
    return r_json


def show_current_weather():
    temp = round((get_weather())['current']['temp'], 0)
    # a = ((get_weather())['current']['weather'][0]['main'])
    # b = ((get_weather())['current']['weather'][0]['description'])
    return f'Сейчас в Киеве температура воздуха: {temp}.'


def show_tomorrow_weather():
    temp_min = round((get_weather())['daily'][1]['temp']['min'], 0)
    temp_max = round((get_weather())['daily'][1]['temp']['max'], 0)
    return f'Завтра в Киеве температура воздуха: мин.+{temp_min}, макс.+{temp_max}.'


def write_json(data, filename='weather.json'):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


if __name__ == '__main__':
    save_weather_json()