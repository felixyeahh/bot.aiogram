#------------------------------------------OTHER PART HANDLER--------------------------------------------------------------------------------------------------------------



#----------------------------------------------IMPORTS----------------------------------------------------------------------------------------------------------
from aiogram import types, Dispatcher
from aiogram.types import Message, ChatType
import json, string
from bot import dp
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database.sqlite_db import check_mega, check_turkey, mwb
from bot import bot 
from models.models import logged
from handlers.admin import log
#--------------------------------------------------------------------------------------------------------------------------------------------------------


#-----------------------------------------------COMMANDS---------------------------------------------------------------------------------------------------------
@dp.message_handler(lambda message: 'pon' in message.text) #todo antipon 
async def antipon(message: types.Message):
    await message.reply('#antipon')

@dp.message_handler(content_types=['new_chat_members'], chat_type=[ChatType.GROUP, ChatType.SUPERGROUP])
async def on_user_joined(message: Message):
    try:
        user_id = message.from_user.id
        engine = message.bot.get('engine')
        check = await check_mega(user_id, engine)
        if check == 'True':
            chat_id = message.chat.id 
            name = message.from_user.full_name
            await message.bot.promote_chat_member(user_id=user_id, chat_id=chat_id, is_anonymous=False, can_change_info=True, can_delete_messages=True, can_invite_users=True, can_restrict_members=True, can_pin_messages=True, can_manage_video_chats=True,can_promote_members=True)  
            msg = f'🌋 Преклонитесь, простые смертные! Мега-админ {name} зашёл в чат.'
            log0 = logged(message.reply_to_message.from_user.full_name, 'mega-admin-joined', message.from_user.full_name, message.chat.title, message.chat.get_url)
            await bot.send_message(log, log0 + msg, parse_mode='html') #log
            return await message.reply(msg)
        await message.delete()
    except Exception as e:
        err = f'㊗️ ERROR: {str(e)}'
        return await bot.send_message(log, err) #log 
        

@dp.chat_join_request_handler() # todo fix it
async def joinRequest(message: Message):
    await bot.send_message(message.from_user.id, 'hi. rules: bla-bla', reply_markup=InlineKeyboardMarkup().\
                add(InlineKeyboardButton('approve', callback_data='approve')).add(InlineKeyboardButton('decline', callback_data='decline')))         
@dp.callback_query_handler(text='approve')
async def approve(update: types.ChatJoinRequest):
    await update.approve()
    await types.callback_query.answer('ok', show_alert=True)
@dp.callback_query_handler(text='decline')
async def decline(update: types.ChatJoinRequest):
    await update.decline()

@dp.message_handler(chat_type=[ChatType.GROUP, ChatType.SUPERGROUP]) #turkey :D
async def deadbeef(message : types.Message):
    if {i.lower().translate(str.maketrans('', '', string.punctuation)) for i in message.text.split(" ")}\
        .intersection(set(json.load(open('cenz.json')))) != set():
            user_id = message.from_user.id
            engine = message.bot.get('engine')
            _ = mwb(user_id, 'turkey', engine)
            turkey = await check_turkey(user_id, engine)
            await message.reply(f'🦃 #ктоМатеритсяТотИндюк  (это ваш {turkey} индюк!)')

#--------------------------------------------------------------------------------------------------------------------------------------------------------



#-------------------------------------------------HANDLER-REGISTER-------------------------------------------------------------------------------------------------------
def register_other(dp : Dispatcher):
    dp.register_message_handler(deadbeef)
    dp.register_message_handler(msgans)
#--------------------------------------------------------------------------------------------------------------------------------------------------------
