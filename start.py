
# ? ---------imports
from bot import bot, dp, Bot
from aiogram import Dispatcher, utils
from handlers import client, admin, other, roleplay
from database import sqlite_db
from servises.set_comm import set_default_commands
from database.sqlite_db import get_engine, create_database

async def set_all_default_commands(bot: Bot): # ? setting-commands
    await set_default_commands(bot)
async def create_db(bot: Bot): # ? creating-database
    sqlite_file_name = 'ench.db'
    sqlite_url = f'sqlite:///{sqlite_file_name}'
    engine = get_engine(sqlite_url)
    create_database(engine)
    bot['engine'] = engine

async def on_startup(dispatcher: Dispatcher): # ? on-startup
    sqlite_db.sql_start()
    await create_db(dispatcher.bot)
    await set_all_default_commands(dispatcher.bot)
    await bot.send_message(-1001847368960, '>>> bot connected')
    
# ? -----------registering-handlers
client.register_client(dp)
admin.register_admin(dp)
other.register_other(dp)


utils.executor.start_polling(dp, skip_updates=True, on_startup=on_startup) # ! starting the bot
