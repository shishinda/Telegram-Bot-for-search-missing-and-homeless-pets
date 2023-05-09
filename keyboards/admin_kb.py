from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

#Кнопки клавиатуры админа
button_load = KeyboardButton('/Новая_заявка')
button_load2 = KeyboardButton('/Заявка_из_питомника')
button_delete = KeyboardButton('/Удалить')
button_delete2 = KeyboardButton('/Удаление_заявки_питомник')

button_case_admin = ReplyKeyboardMarkup(resize_keyboard=True).add(button_load).insert(button_load2).insert(button_delete) \
    .row(button_delete2)