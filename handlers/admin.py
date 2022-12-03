#------------------------------------IMPORTS-------------------
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from bot import dp, bot
from aiogram.dispatcher.filters import Text
from database import sqlite_db
from database.sqlite_db import sql_del_command, sql_add_command, sql_read, sql_read2
from keyboard import adm_kb
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
#-----------------------------------------------------------------------------


#---------------------------------------------------------FSMContext-----------------------------------------------------------------------------------------------
class fyTasks(StatesGroup): 
    name = State()
    desc = State()
    reward = State()

aid = 118198979 #admin id

@dp.message_handler(lambda message: '!getkb' in message.text) #get admin keyboard
async def getrights(message: types.Message):
    global aid
    if message.from_user.id == aid:
        await message.reply('done.', reply_markup=adm_kb.akb)
    else: 
        await message.reply('you are not admin lol bro')


@dp.message_handler(lambda message: 'add' in message.text)
async def fyStartTasks(message: types.Message):
    if message.from_user.id == aid:
        await fyTasks.name.set()
        await message.reply('🤠  working successfully. Now, enter task name')

@dp.message_handler(state='fyTasks', commands='killstate')
@dp.message_handler(Text(equals='cancel', ignore_case=False), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    if message.from_user.id == aid:
        current_state = await state.get_state()
        if current_state is None:
            return
        await state.finish()
        await message.reply('👽 State killed successfully')

@dp.message_handler(state=fyTasks.name)
async def load_name(message: types.Message, state: FSMContext):
    if message.from_user.id == aid:
        async with state.proxy() as data:
            data['name'] = message.text
        await fyTasks.next()
        await message.reply('🪸 Enter content of your task.')

@dp.message_handler(state=fyTasks.desc)
async def load_desc(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['desc'] = message.text
    await fyTasks.next()
    await message.reply('enter reward')

@dp.message_handler(state=fyTasks.reward)
async def load_price(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['reward'] = message.text
    await sqlite_db.sql_add_command(state) #saving info to db
    await state.finish() #finish FSM
#--------------------------------------------------------------------------------------------------------------------------------------------------------


#-------------------------------------------------------ADMIN COMMANDS-------------------------------------------------------------------------------------------------
@dp.callback_query_handler(lambda x: x.data and x.data.startswith('del ')) #del info inline button 
async def delcall(callback: types.CallbackQuery):
    await sqlite_db.sql_del_command(callback.data.replace('del ', ' '))
    await callback.answer(text=f'{callback.data.replace("del ", "")} deleted', show_alert=True)

@dp.message_handler(lambda message: 'del' in message.text) #del info
async def delete_from_db(message: types.Message):
    global aid 
    if message.from_user.id == aid: 
        read = await sqlite_db.sql_read2()
        for ret in read:
            await bot.send_message(message.from_user.id, f'{ret[0]}\n{ret[1]}\n{ret[2]}', reply_markup=InlineKeyboardMarkup().\
                add(InlineKeyboardButton(f'delete {ret[0]}', callback_data=f'del {ret[0]}')))
#--------------------------------------------------------------------------------------------------------------------------------------------------------



#-------------------------------------------------------REGISTER-HANDLERS-------------------------------------------------------------------------------------------------
def register_admin(dp : Dispatcher):
    dp.register_message_handler(fyStartTasks)
    dp.register_message_handler(load_name, state=fyTasks.name)
    dp.register_message_handler(load_desc, state=fyTasks.desc)
    dp.register_message_handler(load_price, state=fyTasks.reward)
    dp.register_callback_query_handler(delcall)
    dp.register_message_handler(delete_from_db)
    dp.register_message_handler(cancel_handler, state='fyTasks', commands=["killstate"])
#--------------------------------------------------------------------------------------------------------------------------------------------------------