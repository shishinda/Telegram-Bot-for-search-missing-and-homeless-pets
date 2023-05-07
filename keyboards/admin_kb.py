from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

#Кнопки клавиатуры админа
button_load = KeyboardButton('/Новая_заявка')
button_delete = KeyboardButton('/Удалить')

button_case_admin = ReplyKeyboardMarkup(resize_keyboard=True).add(button_load)\
    .add(button_delete)