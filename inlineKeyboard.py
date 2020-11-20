# файл отвечает за разметку всплывающих кнопок сообщения
import telebot
import emoji

inline_btn_menu_geo = telebot.types.InlineKeyboardButton(emoji.emojize(':world_map: Настройка местоположения'),
                                                         callback_data='menu_btn_geo')
inline_btn_menu_notify = telebot.types.InlineKeyboardButton(emoji.emojize(':alarm_clock: Выбор времени уведомлений'),
                                                            callback_data='menu_btn_notify')
inline_kb_settings = telebot.types.InlineKeyboardMarkup(row_width=1).add(inline_btn_menu_geo,
                                                                         inline_btn_menu_notify)
all_btn = [telebot.types.InlineKeyboardButton(emoji.emojize(f':one-thirty: {i:02d}:00'), callback_data=f'btn{i:02d}:00')
           for i in range(5, 23)]
all_btn.append(telebot.types.InlineKeyboardButton(emoji.emojize('Ввести вручную'), callback_data='btn_edit'))
btn_tuple_data = [f'btn{i:02d}:00' for i in range(5, 23)]
btn_tuple_data.append('btn_edit')
inline_kb_all_times = telebot.types.InlineKeyboardMarkup().add(*all_btn)
