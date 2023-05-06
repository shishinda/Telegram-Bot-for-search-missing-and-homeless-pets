from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

b1 = KeyboardButton('/help')
b2 = KeyboardButton('/start')
b3 = KeyboardButton('/Активные_заявки')

kb_client = ReplyKeyboardMarkup(resize_keyboard=True)

kb_client.add(b1).insert(b2).insert(b3)