from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram import types, Dispatcher
from create_bot import dp, bot
from data_base import sqlite_db
from keyboards import admin_kb
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


ID = None

class FSMAdmin(StatesGroup):
    pets_name = State()
    breed = State()
    signs = State()
    photo = State()
    owner_name = State()
    owner_phone = State()

#Получаем ID текущего модератора
#@dp.message_handler(commands=['moderator'], is_chat_admin=True)
async def make_changes_command(message: types.Message):
    global ID
    ID = message.from_user.id
    await bot.send_message(message.from_user.id, 'Ожидаю команды администратора', reply_markup=admin_kb.button_case_admin)
    await message.delete()

#Начало диалога загрузки новой заявки
#@dp.message_handler(commands='Новая_заявка', state=None)
async def cm_start(message : types.Message):
    if message.from_user.id == ID:
        await FSMAdmin.pets_name.set()
        await message.reply("Укажите кличку животного")

#Отмена
#@dp.message_handler(state="*", commands='отмена')
#@dp.message_handler(Text(equals='отмена', ignore_case=True), state="*")
async def cansel_handler(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        current_state = await state.get_state()
        if current_state is None:
            return
        await state.finish()
        await message.reply('Отмена операции')

#Ловим первый ответ и записываем его в словарь
#@dp.message_handler(state=FSMAdmin.pets_name)
async def load_pets_name(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['pets_name'] = message.text
        await FSMAdmin.next()
        await message.reply("Укажите породу животного")

#Ловим второй ответ
#@dp.message_handler(state=FSMAdmin.breed)
async def load_breed(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['breed'] = message.text
        await FSMAdmin.next()
        await message.reply("Укажите отличительные признаки животного")

#Ловим третий ответ
#@dp.message_handler(state=FSMAdmin.signs)
async def load_signs(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['signs'] = message.text
        await FSMAdmin.next()
        await message.reply("Загрузите фото животного")

#Ловим четвертый ответ
#@dp.message_handler(content_types=['photo'], state=FSMAdmin.photo)
async def load_photo(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['photo'] = message.photo[0].file_id
        await FSMAdmin.next()
        await message.reply("Введите имя хозяина")

#Ловим пятый ответ
#@dp.message_handler(state=FSMAdmin.owner_name)
async def load_owner_name(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['owner_name'] = message.text
        await FSMAdmin.next()
        await message.reply("Введите телефон хозяина")

#Ловим шестой ответ и используем полученные данные
#@dp.message_handler(state=FSMAdmin.owner_phone)
async def load_owner_phone(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['owner_phone'] = int(message.text)

        await sqlite_db.sql_add_command(state)
        await state.finish()

@dp.callback_query_handler(lambda x: x.data and x.data.startswith('del'))
async def del_callback_run(callback_querry: types.CallbackQuery):
    await sqlite_db.sql_delete_command(callback_querry.data.replace('del ', ''))
    await callback_querry.answer(text=f'Заявка на поиск {callback_querry.data.replace("del ", "")} удалена', show_alert=True)

#@dp.message_handler(commands='Удалить')
async def delete_item(message: types.Message):
    if message.from_user.id == ID:
        read = await sqlite_db.sql_read2()
        for ret in read:
            await bot.send_photo(message.from_user.id, ret[3], f'Кличка животного:{ret[0]}\nПорода:{ret[1]}\nПриметы:{ret[2]}\nИмя хозяина:{ret[4]}\nТелефон хозяина:{ret[5]}')
            await bot.send_message(message.from_user.id, text='^^^', reply_markup=InlineKeyboardMarkup().\
                                   add(InlineKeyboardButton(f'Удалить заявку на поиск {ret[0]}', callback_data=f'del {ret[0]}')))

#Регистрируем хэндлеры
def register_handlers_admin(dp : Dispatcher):
    dp.register_message_handler(cm_start, commands=['Новая_заявка'], state=None)
    dp.register_message_handler(cansel_handler, state="*", commands='отмена')
    dp.register_message_handler(cansel_handler, Text(equals='отмена', ignore_case=True), state="*")
    dp.register_message_handler(load_pets_name, state=FSMAdmin.pets_name)
    dp.register_message_handler(load_breed, state=FSMAdmin.breed)
    dp.register_message_handler(load_signs, state=FSMAdmin.signs)
    dp.register_message_handler(load_photo, content_types=['photo'], state=FSMAdmin.photo)
    dp.register_message_handler(load_owner_name, state=FSMAdmin.owner_name)
    dp.register_message_handler(load_owner_phone, state=FSMAdmin.owner_phone)
    dp.register_message_handler(make_changes_command, commands=['moderator'], is_chat_admin=True)
    dp.register_message_handler(delete_item, commands=['Удалить'])



