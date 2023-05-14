from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

#Кнопки клавиатуры админа
button_load = KeyboardButton('/Новая_заявка')
button_load2 = KeyboardButton('/Заявка_из_питомника')
button_read = KeyboardButton('/Поданные_заявки')
button_delete = KeyboardButton('/Удалить')
button_delete2 = KeyboardButton('/Удаление_заявки_питомник')
button_delete3 = KeyboardButton('/Удалить_поданные_заявки')

button_case_admin = ReplyKeyboardMarkup(resize_keyboard=True).add(button_load).insert(button_load2).insert(button_delete) \
    .row(button_delete2).row(button_read).row(button_delete3)