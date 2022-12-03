#-------------------------------------------------------------------database-------------------------------------------------------------------------------------


#--------------------------------------------------IMPORTS------------------------------------------------------------------------------------------------------
import sqlite3 as sq
from bot import bot 
#--------------------------------------------------------------------------------------------------------------------------------------------------------


#--------------------------------------------------------------------------------------------------------------------------------------------------------
def sql_start(): 
    global base, cur 
    base = sq.connect('ench_db.db')
    cur = base.cursor()
    if base:
        print("^database connected")
    base.execute('CREATE TABLE IF NOT EXISTS tasks(name TEXT PRIMARY KEY, desc TEXT, reward TEXT) ')

async def sql_add_command(state):
    async with state.proxy() as data:
        cur.execute('INSERT INTO tasks VALUES(?,?,?)', tuple(data.values()))
        base.commit()

async def sql_read(message):
    for ret in cur.execute('SELECT * FROM tasks').fetchall():
        await bot.send_message(message.from_user.id, f'{ret[0]}\n{ret[1]}\n{ret[2]}')

async def sql_read2():
    return cur.execute('SELECT * FROM tasks').fetchall()

async def sql_del_command(data):
    cur.execute('DELETE FROM tasks WHERE name == ?', (data,))
    base.commit()
#--------------------------------------------------------------------------------------------------------------------------------------------------------