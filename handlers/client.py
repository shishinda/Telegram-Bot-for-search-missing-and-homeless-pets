from aiogram import types, Dispatcher
from create_bot import dp, bot
from keyboards import kb_client
from aiogram.types import ReplyKeyboardRemove

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

#@dp.message_handler(commans=['Активные_заявки'])
#async def active_applications_command(message: types.Message):
#    for

def register_handlers_client(dp : Dispatcher):
    dp.register_message_handler(command_start, commands=['start'])
    dp.register_message_handler(command_help, commands=['help'])