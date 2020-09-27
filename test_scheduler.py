from apscheduler.schedulers.blocking import BlockingScheduler
from bot_handlers import notify_weather

sched = BlockingScheduler()


@sched.scheduled_job('interval', seconds=30)
def timed_job():
    notify_weather()
    print('Тестирование расписания, я вызываюсь кажыде 30 секунд.')


if __name__ == '__main__':
    sched.start()