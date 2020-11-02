# этот файл отвечает за расписание проверки уведомления
from apscheduler.schedulers.background import BlockingScheduler
import bot_handlers


sched = BlockingScheduler()


@sched.scheduled_job('interval', seconds=60)    # вызывается каждые 60 сек
def timed_job():
    bot_handlers.notify_weather()


def start_schedule():
    print('Расписание запущено...')
    sched.start()
