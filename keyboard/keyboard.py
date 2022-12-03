from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

b1 = KeyboardButton('Слава советскому союзу', request_contact=True)
b2 = KeyboardButton('Максим molodets', request_location=True)

kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

kb.add(b1).insert(b2)
