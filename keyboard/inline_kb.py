from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

inbut = InlineKeyboardButton(text='Press F to Pay Respect', callback_data='prf')
inbut1 = InlineKeyboardButton(text='What Can You Do?',callback_data='aldolist')
inbut2 = InlineKeyboardButton(text='Who is your creator?', callback_data='felix')
inbut3 = InlineKeyboardButton(text='Do NOT Press This Button', callback_data='donot')
inkb = InlineKeyboardMarkup(row_width=2).add(inbut, inbut1, inbut2, inbut3)