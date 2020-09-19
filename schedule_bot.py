import datetime
import time
import schedule
import weather_api
import bot_handlers
import db
from bot_config import bot


def notify_weather_15_00():
    time_now = datetime.datetime.now().strftime('%H:%M')
    list_tuples_id_users = db.list_id_users_in_db()
    list_id_users = []
    for tuple_in_list in list_tuples_id_users:
        list_id_users.append(tuple_in_list[1])
    for user_id_in_list in list_id_users:
        if db.get_time_notify_user_db(user_id=user_id_in_list) == time_now:
            bot.send_message(chat_id=user_id_in_list, text=weather_api.show_current_daily_weather())


