import time
import schedule
import weather_api
import bot
import bot_handlers


schedule.every().day.at("00:42").do(weather_api.show_current_daily_weather())

# нужно иметь свой цикл для запуска планировщика с периодом в 1 секунду:
if __name__ == '__main__':

    while True:
        schedule.run_pending()
        time.sleep(1)