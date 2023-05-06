from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

#Кнопки клавиатуры админа
button_load = KeyboardButton('/Загрузить_данные')
button_delete = KeyboardButton('/Удалить_данные')

button_case_admin = ReplyKeyboardMarkup(resize_keyboard=True).add(button_load)\
    .add(button_delete)