#--------------------------------------------------CLIENT PART HANDLER----------------------------------------------------------------------


#-----------------------------------------------------IMPORTS--------------------------------------------------------------------------------------------
from aiogram import types, Dispatcher
from bot import dp
from keyboard import inkb 
from database.sqlite_db import check_balance, check_turkey, sql_read
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types import Message, ChatType
from aiogram.dispatcher.filters import Text
#--------------------------------------------------------------------------------------------------------------------------------------------------------


# ? ------start cmd + callbacks 
@dp.message_handler(commands=['start'], chat_type=[ChatType.PRIVATE])
async def startcmd(message : types.Message):
    try:
        await message.answer('Привет! Я - bot.aiogram, бот написаный для себя, чтоб создатель поумнел чутка.', reply_markup=inkb)
    except:
        await message.delete()
@dp.callback_query_handler(text='prf')
async def pressf(callback: types.callback_query):
    await callback.answer('you pressed F', show_alert=True)
@dp.callback_query_handler(text='aldolist')
async def dolist(callback: types.CallbackQuery):
    await callback.message.answer('''todo: update it''')
    await callback.answer('check it out')
@dp.callback_query_handler(text='felix')
async def felix(callback: types.callback_query):
    await callback.message.answer('my creator is Felix.', reply_markup=InlineKeyboardMarkup().\
        add(InlineKeyboardButton('His Channel', url = 't.me/felixyeah'), InlineKeyboardButton('His Group', url='https://t.me/+89m5WL5W6zA4NDli')))
    await callback.answer()
@dp.callback_query_handler(text='donot')
async def donot(callback: types.callback_query):
    await callback.answer('Nu i nahui ti najal, loh tupoy', show_alert=True)

@dp.message_handler(commands=['info', 'chatinfo'], commands_prefix='.!/*') #todo get chat info
async def chatinfo(message: Message):
    if not message.reply_to_message:
        title = message.chat.title
        id = message.chat.id 
        photo = message.chat.photo[0].file_id

@dp.message_handler(Text(equals='my balance', ignore_case=True))
async def mybalance(message: Message): #todo reply to user
    engine = message.bot.get('engine')
    user_id = message.from_user.id
    balance = await check_balance(user_id, engine)
    name = message.from_user.full_name
    return await message.reply(f'💎 Ваш баланс: {balance} поинтов. | {name}')

@dp.message_handler(Text(equals="сколько индюков?", ignore_case=True))
async def myturkey(message: Message):
    engine = message.bot.get('engine')
    if not message.reply_to_message: 
        user_id = message.from_user.id
        name = message.from_user.full_name
    else:
        name = message.reply_to_message.from_user.full_name
        user_id = message.reply_to_message.from_user.id
    turkey = await check_turkey(user_id, engine)
    garden = '🦃' * int(turkey)
    if turkey < 1:
        return await message.reply(f'😵‍💫 Ой-ой! {name} живет совсем без индюков!')
    else:
        return await message.reply(f'🏡 {name}, обыскиваем ваш дом…. \n\n\n 🦃 Найдено {turkey} индюков\n\n\n' + garden)

@dp.message_handler(commands=['quests'], commands_prefix='!/') # db reader #todo if chatType=group send message...
async def dbcheck(message: types.Message):
    await sql_read(message)

@dp.message_handler(commands='id', commands_prefix='/!*') #get user_id
async def getid(message: Message):
    if not message.reply_to_message: 
        user_id = message.from_user.id
        name = message.from_user.full_name
    else:
        name = message.reply_to_message.from_user.full_name
        user_id = message.reply_to_message.from_user.id
    
    return await message.reply(f'#️⃣ {name} ID: <code> {user_id} </code>', parse_mode='html')
#--------------------------------------------------------------------------------------------------------------------------------------------------------



#---------------------------------------------------------REGISTER-HANDLER-----------------------------------------------------------------------------------------------
def register_client(dp : Dispatcher):
    dp.register_message_handler(startcmd, commands=['start'])
    
