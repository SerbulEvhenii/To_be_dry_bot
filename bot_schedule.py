# этот файл отвечает за расписание проверки уведомления
from apscheduler.schedulers.background import BlockingScheduler
import bot_handlers
import re

sched = BlockingScheduler()


@sched.scheduled_job('interval', seconds=60)    # вызывается каждые 60 сек
def timed_job():
    bot_handlers.notify_weather()


def start_schedule():
    print('Расписание запущено...')
    sched.start()


def check_valid_time(t: str) -> bool:
    valid = '(\d{2}):(\d{2})'
    if re.match(valid, t): # проверка на колличество введенных цифр между символом :
        find_time = re.findall(valid, t)
        first_part, second_part = find_time[0][0], find_time[0][1]
        if int(first_part) <= 23 and int(second_part) <= 59: # проверка отдельных частей на верность ввода
            return True
        else:
            return False
    else:
        return False
