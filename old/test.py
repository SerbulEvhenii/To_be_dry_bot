import datetime
import threading
import os
import bot_schedule
import db_postgreSQL as db                # Импортируем все методы из файла для базы данных
import weather_api                        # Импортируем все методы из файла для погоды
import telebot.types                      # Импортируем типы телеграма API
import markups                            # Импортируем кнопки для бота
import inlineKeyboard                     # Импортируем инлайн кавиатуры
import emoji                              # Импортируем смайлы http://www.unicode.org/emoji/charts/full-emoji-list.html
from flask import Flask, request, Response
from telebot import types, TeleBot
import geo_position
from flask import send_from_directory
from flask import render_template
from geopy.geocoders import Nominatim
from db_postgreSQL import set_city_user_db

def set_city_geopy(user_id, latit, long):
    geolocator = Nominatim(user_agent="SEA")
    location = geolocator.reverse(f"{latit}, {long}", language='ru')
    if location:
        loc_dict = location.raw
        city = loc_dict['address']['city'] + ', ' + loc_dict['address']['country']
        set_city_user_db(user_id=user_id, geopy_city=city)
        return True
    else:
        return False


@bot.message_handler(content_types=["location"])
def location(message):
    if message.location is not None:
        if geo_position.set_city_geopy(user_id=message.chat.id, latit=message.location.latitude, long=message.location.longitude):
            db.set_geoposition(user_id=message.chat.id, latit=message.location.latitude, long=message.location.longitude)
            geo_position.set_city_geopy(user_id=message.chat.id, latit=message.location.latitude, long=message.location.longitude)
            bot.send_message(message.chat.id, "Отлично! Я запомнил в каком городе ты находишься. Теперь я буду показывать "
                                              "погоду для твоего города.",
                                              reply_markup=markups.markup_main)
        else:
            bot.send_message(message.chat.id,
                             emoji.emojize(":pensive face: Извините, сервис определения местоположения временно "
                                           "недоступен, попробуйте еще раз немного позже."),
                             reply_markup=markups.markup_main)




