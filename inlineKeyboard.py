import telebot

inline_btn_menu_geo = telebot.types.InlineKeyboardButton('Настройки местоположения', callback_data='menu_btn_geo')
inline_btn_menu_notify = telebot.types.InlineKeyboardButton('Выбор времени уведомлений',
                                                            callback_data='menu_btn_notify')
inline_kb_settings = telebot.types.InlineKeyboardMarkup(row_width=1).add(inline_btn_menu_geo,
                                                                         inline_btn_menu_notify)

inline_btn_1 = telebot.types.InlineKeyboardButton('05:00', callback_data='btn05:00')
inline_btn_2 = telebot.types.InlineKeyboardButton('06:00', callback_data='btn06:00')
inline_btn_3 = telebot.types.InlineKeyboardButton('07:00', callback_data='btn07:00')
inline_btn_4 = telebot.types.InlineKeyboardButton('08:00', callback_data='btn08:00')
inline_btn_5 = telebot.types.InlineKeyboardButton('09:00', callback_data='btn09:00')
inline_btn_6 = telebot.types.InlineKeyboardButton('10:00', callback_data='btn10:00')
inline_btn_7 = telebot.types.InlineKeyboardButton('11:00', callback_data='btn11:00')
inline_btn_8 = telebot.types.InlineKeyboardButton('12:00', callback_data='btn12:00')
inline_btn_9 = telebot.types.InlineKeyboardButton('13:00', callback_data='btn13:00')
inline_btn_10 = telebot.types.InlineKeyboardButton('14:00', callback_data='btn14:00')
inline_btn_11 = telebot.types.InlineKeyboardButton('15:00', callback_data='btn15:00')
inline_btn_12 = telebot.types.InlineKeyboardButton('16:00', callback_data='btn16:00')
inline_btn_13 = telebot.types.InlineKeyboardButton('17:00', callback_data='btn17:00')
inline_btn_14 = telebot.types.InlineKeyboardButton('18:00', callback_data='btn18:00')
inline_btn_15 = telebot.types.InlineKeyboardButton('19:00', callback_data='btn19:00')
inline_btn_16 = telebot.types.InlineKeyboardButton('20:00', callback_data='btn20:00')
inline_btn_17 = telebot.types.InlineKeyboardButton('21:00', callback_data='btn21:00')
inline_btn_18 = telebot.types.InlineKeyboardButton('22:00', callback_data='btn22:00')
inline_btn_19 = telebot.types.InlineKeyboardButton('23:00', callback_data='btn23:00')

btn_tuple_data = ('btn05:00', 'btn06:00', 'btn07:00', 'btn08:00', 'btn09:00', 'btn10:00', 'btn11:00', 'btn12:00',
                  'btn13:00', 'btn14:00', 'btn15:00', 'btn16:00', 'btn17:00', 'btn18:00', 'btn19:00', 'btn20:00',
                  'btn21:00', 'btn22:00', 'btn23:00'
                  )

inline_kb_all_times = telebot.types.InlineKeyboardMarkup().add(inline_btn_1, inline_btn_2, inline_btn_3, inline_btn_4,
                                                               inline_btn_5, inline_btn_6, inline_btn_7, inline_btn_8,
                                                               inline_btn_9, inline_btn_10, inline_btn_11,
                                                               inline_btn_12,
                                                               inline_btn_13, inline_btn_14, inline_btn_15,
                                                               inline_btn_16,
                                                               inline_btn_17, inline_btn_18, inline_btn_19)
