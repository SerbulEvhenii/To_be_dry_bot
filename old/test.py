import re

alarm = "01:09"
valid = '(\d{2}):(\d{2})'


def check_valid_time(validation, t):
#     if re.match(validation, t): # проверка на колличество введенных цифр между символом :
#         print('ok')
#         find_time = re.findall(validation, t)
#         print(find_time)
#         print(find_time[0][0])
#         print(find_time[0][1])
#         first_part, second_part = find_time[0][0], find_time[0][1]
#         if int(first_part) <= 23 and int(second_part) <= 59: # проверка отдельных частей на верность ввода
#             print('ok, ok!')
#         else:
#             print('Baaad!')
#     else:
#         print('Baaad!')


    if re.match(validation, t):  # проверка на колличество введенных цифр между символом :
        find_time = re.findall(validation, t)
        first_part, second_part = find_time[0][0], find_time[0][1]
        if int(first_part) <= 23 and int(second_part) <= 59:  # проверка отдельных частей на верность ввода
            return True
        else:
            return False
    else:
        return False


if __name__ == '__main__':
    if check_valid_time(valid, alarm):
        print('True')
    else:
        print('False')
