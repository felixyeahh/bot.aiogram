from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
 
load = KeyboardButton('add')
unload = KeyboardButton('del')


akb = ReplyKeyboardMarkup(resize_keyboard=True).add(load)\
    .add(unload) 