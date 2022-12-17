#------------------------------------------------------imports----------------------------------------------------
from aiogram.utils import executor
from bot import dp
from handlers import client, admin, other
from database import sqlite_db
from filters.admin import IsAdminFilter
from servises.set_comm import set_default_commands
from database.sqlite_db import get_engine, create_database
#--------------------------------------------------------------------------------------------------------------------------------------------------------

logger = logging.getLogger(__name__)

def register_all_middlewares(dispatcher: Dispatcher):
    logger.info('Registering middlewares')


def register_all_filters(dispatcher: Dispatcher) -> None:
    logger.info('Registering filters')
    dispatcher.filters_factory.bind(IsAdminFilter)


async def set_all_default_commands(bot: Bot):
    await set_default_commands(bot)
    logger.info('Registering commands')


def create_db(bot: Bot):
    sqlite_file_name = 'ench.db'
    sqlite_url = f'sqlite:///{sqlite_file_name}'
    engine = get_engine(sqlite_url)
    create_database(engine)
    bot['engine'] = engine
    logger.info('Database was created')
    create_db(dispatcher.bot)

#-------------------------------------------------startup-----------------------------
async def on_startup(_):
    print('\n\n\n\n\n^bot connected\n\n\n\n\n')
    sqlite_db.sql_start() #db connect

#handlers-connect
client.register_client(dp)
admin.register_admin(dp)
other.register_other(dp)

executor.start_polling(dp, skip_updates=True, on_startup=on_startup) #start
#--------------------------------------------------------------------------------------------------------------------------------------------------------
