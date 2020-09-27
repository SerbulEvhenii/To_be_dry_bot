import time
import schedule
from bot_handlers import notify_weather

tuple_times = ("05:00", "06:00", "07:00", "08:00", "09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00",
               "16:00", "17:00", "18:00", "19:00", "20:00", "21:00", "22:00", "23:00")

# schedule.every().day.at("05:00").do(notify_weather)
# schedule.every().day.at("06:00").do(notify_weather)
# schedule.every().day.at("07:00").do(notify_weather)
# schedule.every().day.at("08:00").do(notify_weather)
# schedule.every().day.at("09:00").do(notify_weather)
# schedule.every().day.at("10:00").do(notify_weather)
# schedule.every().day.at("11:00").do(notify_weather)
# schedule.every().day.at("12:00").do(notify_weather)
# schedule.every().day.at("13:00").do(notify_weather)
# schedule.every().day.at("14:00").do(notify_weather)
# schedule.every().day.at("15:00").do(notify_weather)
# schedule.every().day.at("16:00").do(notify_weather)
# schedule.every().day.at("17:00").do(notify_weather)
# schedule.every().day.at("18:00").do(notify_weather)
# schedule.every().day.at("19:00").do(notify_weather)
# schedule.every().day.at("20:00").do(notify_weather)
# schedule.every().day.at("21:00").do(notify_weather)
# schedule.every().day.at("22:00").do(notify_weather)
# schedule.every().day.at("23:00").do(notify_weather)
schedule.every(1).minutes.do(notify_weather)

print('Расписание запущено...')

while True:
    schedule.run_pending()
    time.sleep(1)