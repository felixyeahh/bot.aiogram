#--------------------------------------------------CLIENT PART HANDLER----------------------------------------------------------------------


#-----------------------------------------------------IMPORTS--------------------------------------------------------------------------------------------
from aiogram import types, Dispatcher
from bot import dp
from keyboard import kb
from database import sqlite_db
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
#--------------------------------------------------------------------------------------------------------------------------------------------------------


#-----------------------------------------------------kakaya-to huyna, skoro uberu--------------------------------------------------------------------------------------------
'''   urlkb = InlineKeyboardMarkup(row_width=1)
    urlbut0 = InlineKeyboardButton(text='link0', url='https://example.com')
    urlbut2 = InlineKeyboardButton(text='link', url='https://t.me/ntiban')
    textbut0 = InlineKeyboardButton(text='button0', callback_data='data1')'''

'''@dp.message_handler(lambda message: '!links' in message.text)
async def urllinktest(message: types.Message):
    await message.reply('Here you are:', reply_markup=urlkb)'''

inbut = InlineKeyboardButton(text='Press F to Pay Respect', callback_data='prf')
inbut1 = InlineKeyboardButton(text='What Can You Do?',callback_data='aldolist')
inbut2 = InlineKeyboardButton(text='Who is your creator?', callback_data='felix')
inbut3 = InlineKeyboardButton(text='Do NOT Press This Button', callback_data='donot')
inkb = InlineKeyboardMarkup(row_width=2).add(inbut, inbut1, inbut2, inbut3)
#urlkb, urlbut0, urlbut2, textbut0 = new_func()
#urlkb.add(urlbut0, urlbut2, textbut0)
#--------------------------------------------------------------------------------------------------------------------------------------------------------



#--------------------------------------------------------------START + STRANGE COMMANDS------------------------------------------------------------------------------------------
@dp.message_handler(commands=['start'])
async def startcmd(message : types.Message):
    try:
        await message.answer('Привет! Я - bot.aiogram, бот написаный для себя, чтоб создатель поумнел чутка.', reply_markup=inkb)
    except:
        await message.delete()

@dp.message_handler(lambda message: '!ya lisiy' in message.text)
async def yalisiy(message: types.Message):
    await message.reply("ya toje, brat")

'''@dp.callback_query_handler(text='data1')
async def anycall(callback: types.CallbackQuery):
    await callback.answer('ha ha ha ha ha ha')'''

@dp.message_handler(lambda message: '!check' in message.text) #db reader 
async def dbcheck(message: types.Message):
    await sqlite_db.sql_read(message)

@dp.callback_query_handler(text='prf')
async def pressf(callback: types.callback_query):
    await callback.answer('you pressed F', show_alert=True)

@dp.callback_query_handler(text='aldolist')
async def dolist(callback: types.CallbackQuery):
    await callback.message.answer('''I Can
    1. #ктоматеритьсятотиндюк
    2. #antiпон (skoro)
    3. add and remove some files from db
    4. answer on /start and !ya lisiy
    5. show you some inline buttons and answer on them
    6. --empty--''')
    callback.answer('check it out')

@dp.callback_query_handler(text='felix')
async def pressf(callback: types.callback_query):
    await callback.message.answer('my creator is Felix.', reply_markup=InlineKeyboardMarkup().\
        add(InlineKeyboardButton('His Channel', url = 't.me/felixyeah'), InlineKeyboardButton('His Group', url='https://t.me/+89m5WL5W6zA4NDli')))
    await callback.answer()

@dp.callback_query_handler(text='donot')
async def donot(callback: types.callback_query):
    await callback.answer('Nu i nahui ti najal, loh tupoy', show_alert=True)
#--------------------------------------------------------------------------------------------------------------------------------------------------------



#---------------------------------------------------------REGISTER-HANDLER-----------------------------------------------------------------------------------------------
def register_client(dp : Dispatcher):
    dp.register_message_handler(startcmd, commands=['start'])
    dp.register_message_handler(yalisiy)
    dp.register_message_handler(dbcheck)
    dp.register_callback_query_handler(dolist)
    dp.register_callback_query_handler(pressf)
#   dp.register_callback_query_handler(anycall)
#   dp.register_message_handler(urllinktest)