import datetime
import os
import time

if __name__ == '__main__':


    start = datetime.datetime.now()
    a = [1, 2, 3, 4, 5, 5,6 ,7, 8, 9, 0, 3, 9 ,8]
    for x in a:
        print(x)
    end = datetime.datetime.now()
    print(start)
    print(end)
    print(end - start)

    min = datetime.timedelta(minutes=10)
    delta = start + min

    if start > delta:
        print('прошло 10 мин')
    elif start < delta:
        print('еще не прошло 10 мин')

    print(os.path.getctime('weather.json'))
    date_save = time.ctime(os.path.getmtime('weather.json'))
    print(date_save[-13:-5])
    print(min)

    save_10 = datetime.datetime.now() + datetime.timedelta(minutes=10)
    print('save_10 -- ', save_10)
    last_save_file = datetime.datetime.fromtimestamp(os.path.getmtime('weather.json')) + datetime.timedelta(minutes=10)
    print('c -- ', last_save_file)
    # last_save_file += datetime.timedelta(minutes=10)
    print('last ----', last_save_file)

    if last_save_file > save_10:
        print('прошло 10 мин')
    elif last_save_file < save_10:
        print('еще не прошло 10 мин')
