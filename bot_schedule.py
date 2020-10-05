from apscheduler.schedulers.background import BlockingScheduler
import bot_handlers


sched = BlockingScheduler()


@sched.scheduled_job('interval', seconds=60)
def timed_job():
    bot_handlers.notify_weather()
    # print('Тестирование расписания, я вызываюсь каждые 60 секунд.')


def start_schedule():
    print('Расписание запущено...')
    sched.start()
