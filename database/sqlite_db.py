
# ? ---------------database 

# ? ---------------imports
import sqlite3 as sq
from bot import bot 
from typing import Tuple
import logging 
from typing import Union 
from sqlalchemy import exc
from sqlmodel import SQLModel, Session, create_engine, select
from models.models import User

# ! start 
def create_database(engine: create_engine) -> None:
    SQLModel.metadata.create_all(engine)
def sql_start(): 
    global base, cur 
    base = sq.connect('ench.db')
    cur = base.cursor()
    if base:
        print("^database connected")
    base.execute('CREATE TABLE IF NOT EXISTS tasks(name TEXT PRIMARY KEY, desc TEXT, reward TEXT) ')
def get_engine(path: str) -> create_engine:
    return create_engine(path, echo=False)

# ? ------------users
def get_user(engine: create_engine, user_id: str) -> Union[User, None]:
    logging.info('Getting an user')
    with Session(engine) as session:
        try:
            user = session.exec(select(User).where(User.user_id == user_id)).one()
        except exc.NoResultFound:
            print('User was not founded')
            return None
    print('User was founded')
    return user
def create_user(engine: create_engine, data: dict) -> Union[User, None]:
    logging.info('Creating an user')
    user = User(**data)
    with Session(engine) as session:
        try:
            session.add(user)
            session.commit()
            session.refresh(user)
            logging.info('User was created')
        except exc.CompileError:
            logging.warning('User was not created')
            return None
    return user
def update_user(engine: create_engine, user_id: str, field_name: str, value: int) -> bool:
    logging.info('Updating an user')
    user = get_user(engine, user_id)
    with Session(engine) as session:
        try:
            setattr(user, field_name, value)
            session.add(user)
            session.commit()
            logging.info('User was updating')
        except exc.CompileError:
            logging.warning('User was not updating')
            return False
    return True
def delete_user(engine: create_engine, user_id: str) -> bool:
    logging.info('Deleting an user')
    user = get_user(engine, user_id)
    with Session(engine) as session:
        try:
            session.delete(user)
            session.commit()
            logging.info('User was deleting')
        except exc.CompileError:
            logging.warning('User was not deleted')
            return False
    return True

# ? ------------tasks 
async def sql_add_command(state):
    async with state.proxy() as data:
        cur.execute('INSERT INTO tasks VALUES(?,?,?)', tuple(data.values()))
        base.commit()
async def sql_read(message):
    for ret in cur.execute('SELECT * FROM tasks').fetchall():
        await bot.send_message(message.from_user.id, f'⭐️ {ret[0].upper()}\n {ret[1]}\n⛅️ Reward:{ret[2]}')
    '''  if chat_type == [ChatType.GROUP, ChatType.SUPERGROUP]:
        await message.reply('hui') FIXME '''
async def sql_read2():
    return cur.execute('SELECT * FROM tasks').fetchall()
async def sql_del_command(data):
    cur.execute('DELETE FROM tasks WHERE name == ?', (data,))
    base.commit()

# ? --------------balance manipulations
async def check_balance(user_id : str, engine: object) -> Tuple[bool, str]:
    user = get_user(engine, user_id)
    balance = user.balance
    return balance
async def add_balance(user_id : str, field_name : str, args: str, engine: object):
    if user := get_user(engine, user_id):
        update_user(engine, user_id, field_name, getattr(user, field_name) + int(args))
    else:
        user = create_user(engine, {'user_id': user_id, field_name: int(-args)})
    return
async def minus_balance(user_id: str, field_name : str, args: str, engine: object):
    if user := get_user(engine, user_id):
        update_user(engine, user_id,field_name, getattr(user, field_name) - int(args))
    else:
        user = create_user(engine, {'user_id': user_id, field_name: int(-args)})
    return

# ? ---------------mega admin
def set_mega_admin(engine: create_engine, user_id: str, value: str) -> bool:
    user = get_user(engine, user_id)
    with Session(engine) as session:
        try:
            setattr(user, 'is_admin', value)
            session.add(user)
            session.commit()
        except exc.CompileError:
            logging.warning('User was not updating')
            return False
    return True
async def megaAdmin(user_id: str, engine: object):
    if user := get_user(engine, user_id):
        check = await check_mega(user_id, engine)
        if check == 'False':
            set_mega_admin(engine, user_id, 'True')
        if check == 'True':
            set_mega_admin(engine, user_id, 'False')
    else:
        user = create_user(engine, {'user_id': user_id, 'is_admin': 'True'})
    return
async def check_mega(user_id: str, engine: object) -> str:
    if user := get_user(engine, user_id):
        return user.is_admin

async def sqlrun(message: str): #sqlrun
    msg = message[7:]
    cur.execute(msg)
    base.commit()
    return

# ! penalties 
async def check_warns(user_id: str, engine: object) -> Tuple[bool, int]:
    user = get_user(engine, user_id)
    warns = user.warns
    return (True, 0) if warns == 3 else (False, user.warns)
def mwb(user_id: str, field_name: str, engine: object) -> int: 
    seconds: int
    if user := get_user(engine, user_id):
        update_user(engine, user_id, field_name, getattr(user, field_name) + 1)
        return (getattr(user, field_name) + 1) * 2
    else:
        user = create_user(engine, {'user_id': user_id, field_name: 1})
        return getattr(user, field_name) * 2
async def unwarn(user_id: str, field_name: str, engine: object):
    seconds: int
    if user := get_user(engine, user_id):
        update_user(engine, user_id, field_name, getattr(user, field_name) - 1)
        return (getattr(user, field_name) - 1) * 32
    else:
        user = create_user(engine, {'user_id': user_id, field_name: 0})
        return getattr(user, field_name) * 32
async def check_warns2(user_id: str, engine: object) -> int:
    user = get_user(engine, user_id)
    return user.warns
async def check_turkey(user_id: str, engine: object) -> int:
    user = get_user(engine, user_id)
    if not user:
        user = create_user(engine, {'user_id': user_id, 'turkey': '0'})
    return user.turkey
