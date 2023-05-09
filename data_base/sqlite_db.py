import sqlite3 as sq
from create_bot import bot

def sql_start():
    global base, cur
    base = sq.connect('pets_search.db')
    cur = base.cursor()
    if base:
        print('Data base connected')
    base.execute('CREATE TABLE IF NOT EXISTS applications(pets_name TEXT, breed TEXT, signs TEXT, photo TEXT, owner_name TEXT, owner_phone INT)')
    base.execute('CREATE TABLE IF NOT EXISTS homeless(nursery_name TEXT, nursery_address TEXT, nursery_breed TEXT, nursery_photo TEXT, nursery_animal_name TEXT)')
    base.commit()

async def sql_add_command(state):
    async with state.proxy() as data:
        cur.execute('INSERT INTO applications VALUES (?, ?, ?, ?, ?, ?)', tuple(data.values()))
        base.commit()

async def sql_add_command2(state):
    async with state.proxy() as data:
        cur.execute('INSERT INTO homeless VALUES (?, ?, ?, ?, ?)', tuple(data.values()))
        base.commit()

async def sql_read(message):
    for ret in cur.execute('SELECT * FROM applications').fetchall():
        await bot.send_photo(message.from_user.id, ret[3], f'Кличка животного:{ret[0]}\nПорода:{ret[1]}\nПриметы:{ret[2]}\nИмя хозяина:{ret[4]}\nТелефон хозяина:{ret[5]}')

async def sql_read2():
    return cur.execute('SELECT * FROM applications').fetchall()

async def sql_read3(message):
    for ret in cur.execute('SELECT * FROM homeless').fetchall():
        await bot.send_photo(message.from_user.id, ret[3], f'Название приюта:{ret[0]}\nАдрес приюта:{ret[1]}\nПорода животного:{ret[2]}\nКличка животного:{ret[4]}')

async def sql_read4():
    return cur.execute('SELECT * FROM homeless').fetchall()

async def sql_delete_command(data):
    cur.execute('DELETE FROM applications WHERE pets_name == ?', (data,))
    base.commit()

async def sql_delete_nursery_data(data):
    cur.execute('DELETE FROM homeless WHERE nursery_animal_name == ?', (data,))
    base.commit()