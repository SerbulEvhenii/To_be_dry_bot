import datetime



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

