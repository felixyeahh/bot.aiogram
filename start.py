#------------------------------------------------------imports----------------------------------------------------
from aiogram.utils import executor
from bot import dp
from handlers import client, admin, other
from database import sqlite_db
#--------------------------------------------------------------------------------------------------------------------------------------------------------





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


''' #TODO 
1.
2.
3.
'''
