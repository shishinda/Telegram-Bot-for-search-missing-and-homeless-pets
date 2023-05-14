from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

b1 = KeyboardButton('/help')
b2 = KeyboardButton('/start')
b3 = KeyboardButton('/Активные_заявки')
b4 = KeyboardButton('/Заявки_из_приютов')
b5 = KeyboardButton('/Подать_заявку')

kb_client = ReplyKeyboardMarkup(resize_keyboard=True)

kb_client.add(b1).insert(b2).insert(b5).row(b3).row(b4)