import sqlite3 as sq

def sql_start():
    global base, cur
    base = sq.connect('pets_search.db')
    cur = base.cursor()
    if base:
        print('Data base connected')
    base.execute('CREATE TABLE IF NOT EXISTS applications(pets_name TEXT, breed TEXT, signs TEXT, photo TEXT, owner_name TEXT, owner_phone INT)')
    base.commit()

async def sql_add_command(state):
    async with state.proxe() as data:
        cur.execute('INSERT INTO applications VALUES (?, ?, ?, ?, ?, ?)', tuple(data.values()))
        base.commit()