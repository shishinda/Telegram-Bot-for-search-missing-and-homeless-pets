from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram import types, Dispatcher
from create_bot import dp, bot
from data_base import sqlite_db
from keyboards import kb_client
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


class FSMClient(StatesGroup):
    client_pets_name = State()
    client_pets_breed = State()
    client_pets_signs = State()
    client_pets_photo = State()
    client_name = State()
    client_phone = State()


#@dp.message_handler(commands=['start'])
async def command_start(message : types.Message):
    try:
        await bot.send_message(message.from_user.id, 'Приветствуем Вас в Telegram-боте, созданном для помощи в поисках '
                                                 'пропавших домашних, а также бездомных животных, бродящих по улицам '
                                                 'города Ульяновска', reply_markup=kb_client)
        await message.delete()
    except:
        await message.reply('Взаимодействие с Ботом осуществляется через ЛС, напишите ему: https://t.me/PetsSearchBot')

#@dp.message_handler(commands=['help'])
async def command_help(message: types.Message):
    try:
        await bot.send_message(message.from_user.id, 'Этот бот предназначен для того, чтобы пользователь мог '
                                                     'просматривать уже имеющиеся заявки на поиск и реагировать на '
                                                     'них, а также добавлять новые записи.')
        await message.delete()
    except:
        await message.reply( 'Взаимодействие с Ботом осуществляется через ЛС, напишите ему: https://t.me/PetsSearchBot')

#@dp.message_handler(commands=['Активные_заявки'])
async def search_applications(message : types.Message):
    await sqlite_db.sql_read(message)

#@dp.message_handler(commands=['Заявки_из_приютов'])
async def applications_from_nursery(message : types.Message):
    await sqlite_db.sql_read3(message)


#Начало диалога новой заявки от клиента
#@dp.message_handler(commands='Подать_заявку', state=None)
async def client_application(message: types.Message):
    await FSMClient.client_pets_name.set()
    await message.reply("Укажите кличку животного")

#Отмена
#@dp.message_handler(state="*", commands='отмена')
#@dp.message_handler(Text(equals='отмена', ignore_case=True), state="*")
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply('Отмена операции')

#Ловим первый ответ и записываем его в словарь
#@dp.message_handler(state=FSMClient.client_pets_name)
async def load_client_pets_name(message: types.Message, state: FSMContext):
    async with state.proxy() as client_data:
        client_data['client_pets_name'] = message.text
    await FSMClient.next()
    await message.reply("Укажите породу животного")

#Ловим второй ответ
#@dp.message_handler(state=FSMClient.client_pets_breed)
async def load_client_pets_breed(message: types.Message, state: FSMContext):
    async with state.proxy() as client_data:
        client_data['client_pets_breed'] = message.text
    await FSMClient.next()
    await message.reply("Укажите отличительные признаки животного")

#Ловим третий ответ
#@dp.message_handler(state=FSMClient.client_pets_signs)
async def load_client_pets_signs(message: types.Message, state: FSMContext):
    async with state.proxy() as client_data:
        client_data['signs'] = message.text
    await FSMClient.next()
    await message.reply("Загрузите фото животного")

#Ловим четвертый ответ
#@dp.message_handler(content_types=['photo'], state=FSMClient.client_pets_photo)
async def load_client_pets_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as client_data:
        client_data['client_pets_photo'] = message.photo[0].file_id
    await FSMClient.next()
    await message.reply("Введите имя хозяина")

#Ловим пятый ответ
#@dp.message_handler(state=FSMClient.client_name)
async def load_client_name(message: types.Message, state: FSMContext):
    async with state.proxy() as client_data:
        client_data['client_name'] = message.text
    await FSMClient.next()
    await message.reply("Введите телефон хозяина")

#Ловим шестой ответ и используем полученные данные
#@dp.message_handler(state=FSMAdmin.owner_phone)
async def load_client_phone(message: types.Message, state: FSMContext):
    async with state.proxy() as client_data:
        client_data['client_phone'] = int(message.text)

    await sqlite_db.sql_add_client(state)
    await state.finish()

def register_handlers_client(dp : Dispatcher):
    dp.register_message_handler(command_start, commands='start')
    dp.register_message_handler(command_help, commands='help')
    dp.register_message_handler(search_applications, commands='Активные_заявки')
    dp.register_message_handler(applications_from_nursery, commands='Заявки_из_приютов')
    dp.register_message_handler(client_application, commands='Подать_заявку', state=None)
    dp.register_message_handler(cancel_handler, state="*", commands='отмена')
    dp.register_message_handler(cancel_handler, Text(equals='отмена', ignore_case=True), state="*")
    dp.register_message_handler(load_client_pets_name, state=FSMClient.client_pets_name)
    dp.register_message_handler(load_client_pets_breed, state=FSMClient.client_pets_breed)
    dp.register_message_handler(load_client_pets_signs, state=FSMClient.client_pets_signs)
    dp.register_message_handler(load_client_pets_photo, content_types=['photo'], state=FSMClient.client_pets_photo)
    dp.register_message_handler(load_client_name, state=FSMClient.client_name)
    dp.register_message_handler(load_client_phone, state=FSMClient.client_phone)
