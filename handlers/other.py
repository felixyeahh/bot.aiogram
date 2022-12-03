#------------------------------------------OTHER PART HANDLER--------------------------------------------------------------------------------------------------------------



#----------------------------------------------IMPORTS----------------------------------------------------------------------------------------------------------
from aiogram import types, Dispatcher
import json, string
from bot import dp
# from aiogram.methods import ApproveChatJoinRequest
#--------------------------------------------------------------------------------------------------------------------------------------------------------


#-----------------------------------------------COMMANDS---------------------------------------------------------------------------------------------------------
@dp.message_handler() #turkey :D
async def deadbeef(message : types.Message):
    if {i.lower().translate(str.maketrans('', '', string.punctuation)) for i in message.text.split(" ")}\
        .intersection(set(json.load(open('cenz.json')))) != set():
        await message.reply('кто матерится тот индюк')

# class aiogram.types.chat_join_request.ChatJoinRequest(*, chat: Chat, from_user: User, date: datatime, **extradata)
'''@dp.message_handler(lambda message: 'pon'in message.text)
async def antipon()'''
#--------------------------------------------------------------------------------------------------------------------------------------------------------



#-------------------------------------------------HANDLER-REGISTER-------------------------------------------------------------------------------------------------------
def register_other(dp : Dispatcher):
    dp.register_message_handler(deadbeef)
#--------------------------------------------------------------------------------------------------------------------------------------------------------