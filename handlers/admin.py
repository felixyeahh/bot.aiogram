
# ? ------------imports

from aiogram.dispatcher import FSMContext 
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram import Dispatcher
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, ChatType, CallbackQuery, callback_query, chat_permissions

from bot import dp, bot
from database.sqlite_db import add_balance, check_balance, check_mega, check_warns2, megaAdmin, minus_balance, sql_del_command, sql_add_command, sql_read2, sqlrun, check_warns, mwb, unwarn, add_balance #* database
from keyboard import adm_kb, promote_kb 
from datetime import timedelta
from models.models import logged

#? exceptions
from aiogram.utils.exceptions import NotEnoughRightsToRestrict, MessageCantBeDeleted

# ? --------info
global aid
global log
aid = 118198979 # ? admin id
log = -1001847368960 # ? logging chanel

# ? -----------Everything about Tasks
class fyTasks(StatesGroup): #states group
    name = State()
    desc = State()
    reward = State()
@dp.message_handler(commands=['getkb'], commands_prefix='!*/') #get admin keyboard
async def tasks_keyboard(message: Message):
    name = message.from_user.full_name
    if message.from_user.id == aid:
        await message.reply(f'🌶 Админская клавиатура выдана, {name}!', reply_markup=adm_kb.akb)
    else: 
        await message.reply(f'🙄 Похоже, что ты не админ, {name}.')
@dp.message_handler(Text(equals='add', ignore_case=False)) #adding tasks 
async def fyStartTasks(message: Message):
    if message.from_user.id == aid:
        await fyTasks.name.set()
        await message.reply('🐡 Working successfully! Для начала, введи название задания.')
@dp.message_handler(Text(equals='cancel', ignore_case=True), state='*') #cancel state
async def cancel_state_cmd(message: Message, state: FSMContext):
    if message.from_user.id == aid:
        current_state = await state.get_state()
        if current_state is None:
            return
        await state.finish()
        return await message.reply('👽 State killed successfully')
@dp.message_handler(state=fyTasks.name)
async def load_name(message: Message, state: FSMContext):
    if message.from_user.id == aid:
        async with state.proxy() as data:
            data['name'] = message.text #adding name of task
        await fyTasks.next()
        await message.reply('🪸 Теперь, введи само задание.')
@dp.message_handler(state=fyTasks.desc)
async def load_desc(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['desc'] = message.text #adding content of task
    await fyTasks.next()
    await message.reply('💎 Последний шаг! Введи награду за задание.')
@dp.message_handler(state=fyTasks.reward)
async def load_price(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['reward'] = message.text  #adding reward of task
        await bot.send_message(log, '#newTask: ' + str(data)) #log to log channel
        await message.reply('📟 Успешно сохранено.', reply_markup=InlineKeyboardMarkup().\
            add(InlineKeyboardButton('logs', url='https://t.me/+2iVpbvEzyF83MjNi')))
    await sql_add_command(state) #saving info to db
    await state.finish() #finish FSM
@dp.callback_query_handler(lambda x: x.data and x.data.startswith('del ')) #del info inline button 
async def delcall(callback: CallbackQuery):
    await sql_del_command(callback.data.replace('del ', ' '))
    await callback.answer(text=f'{callback.data.replace("del ", "")} deleted', show_alert=True)
@dp.message_handler(lambda message: 'del' in message.text) #del info #FIXME 
async def delete_from_db(message: Message):
    global aid 
    if message.from_user.id == aid: 
        read = await sql_read2()
        for ret in read:
            await bot.send_message(message.from_user.id, f'⭐️ {ret[0].upper()}\n {ret[1]}\n⛅️ Reward:{ret[2]}', reply_markup=InlineKeyboardMarkup().\
                add(InlineKeyboardButton(f'delete {ret[0]}', callback_data=f'del {ret[0]}')))

async def get_admins(message: Message) -> str: #get admins of group
    chat_id = message.chat.id
    admins = await message.bot.get_chat_administrators(chat_id)
    text = ''
    for admin in admins:
        text += f'@{admin.user.username}\n '
    return text

# ? -----------warns
@dp.message_handler(commands=['warn'], commands_prefix='!/*', is_chat_admin=True, chat_type=[ChatType.GROUP, ChatType.SUPERGROUP])  
async def warn_cmd(message: Message):
    try:
        if not message.reply_to_message:
            return await message.reply('🫥 No reply.')
        await message.delete()
        txt = message.text
        args = txt[4:]
        user_id = message.reply_to_message.from_user.id
        engine = message.bot.get('engine')
        _ = mwb(user_id, 'warns', engine)
        ban, warns = await check_warns(user_id, engine)
        name = message.reply_to_message.from_user.full_name
        admin_name = message.from_user.full_name
        if ban: 
            await message.bot.ban_chat_member(chat_id=message.chat.id, user_id=user_id, until_date=timedelta(seconds=29))
            return await message.reply_to_message.reply(f'👹 {name} словил бан. | Достижение трёх варнов | {admin_name}')
        return await message.reply_to_message.reply(f'💫  {name} получает предупреждение ({warns}/3) | {args} | {admin_name}')
    except Exception as e:
        err = f'㊗️ ERROR: {str(e)}'
        return await bot.send_message(log, err) #log 
@dp.message_handler(commands=['unwarn'], commands_prefix='/!', is_chat_admin=True, chat_type=[ChatType.GROUP, ChatType.SUPERGROUP]) #todo log
async def unwarn_cmd(message: Message):
    try:
        if not message.reply_to_message:
            return await message.reply('🫥 No reply.')
        await message.delete()

        user_id = message.reply_to_message.from_user.id
        engine = message.bot.get('engine')
        _ = await unwarn(user_id, 'warns', engine)
        name = message.reply_to_message.from_user.full_name
        admin_name = message.from_user.full_name
        warns = await check_warns2(user_id, engine)
        return await message.reply_to_message.reply(f'🪷 {name}, мои поздравления, с вас сняли предупреждение! ({warns}/3) | {admin_name}')
    except Exception as e:
        err = f'㊗️ ERROR: {str(e)}'
        await message.reply(err)
        return await bot.send_message(log, err) #log 
# ? ------------balance 
@dp.message_handler(Text(startswith='+'))  
async def plus_cmd(message: Message):
    try:
        txt = message.text
        args = txt.split('+')
        args = args[1]
        if message.from_user.id == aid:
            if not message.reply_to_message:
                return await message.reply('🫥 No reply.')
            user_id = message.reply_to_message.from_user.id 
            engine = message.bot.get('engine')
            _ = await add_balance(user_id, 'balance', args, engine)
            balance = await check_balance(user_id, engine)
            log0 = logged(message.reply_to_message.from_user.full_name, 'plus balance',message.from_user.full_name, message.chat.title, message.chat.get_url)
            msg = f'🔰 <i>{message.reply_to_message.from_user.full_name}, зачислено {args} поинтов! Твой текущий баланс:</i><b> {balance}</b>'
            await bot.send_message(log, log0 + msg, parse_mode='html')
            return await message.reply_to_message.reply(msg)
        else:
            return
    except Exception as e:
        err = f'㊗️ ERROR: {str(e)}'
        return await bot.send_message(log, err) #log 
@dp.message_handler(Text(startswith='-'))  
async def minus_cmd(message: Message):
    try:
        txt = message.text
        args = txt.split('-')
        args = args[1]
        if message.from_user.id == aid:
            name = message.reply_to_message.from_user.full_name
            if not message.reply_to_message:
                return await message.reply('🫥 No reply.')
            user_id = message.reply_to_message.from_user.id 
            engine = message.bot.get('engine')
            _ = await minus_balance(user_id, 'balance', args, engine)
            balance = await check_balance(user_id, engine)
            log0 = logged(message.reply_to_message.from_user.full_name, 'minus balance', message.from_user.full_name, message.chat.title, message.chat.get_url)
            msg = f'<i>🥶 {name}, {message.from_user.full_name} украл у вас {args} поинтов! Твой текущий баланс: </i><b>{balance}</b>.'
            await bot.send_message(log, log0 + msg, parse_mode='html')
            return await message.reply_to_message.reply(msg, parse_mode='html')
        else:
            return
    except Exception as e:
        err = f'㊗️ ERROR: {str(e)}'
        return await bot.send_message(log, err) #log 

# ? ------------ban
@dp.message_handler(commands=['ban', 'kick'], commands_prefix='.*/!', is_chat_admin=True) #todo log
async def ban_cmd(message: Message):
    try: 
        if not message.reply_to_message:
            await message.reply('🫥 No reply.')
            return
        args = message.text.split()
        name = message.reply_to_message.from_user.full_name
        admin_name = message.from_user.full_name
        user_id = message.reply_to_message.from_user.id
        engine = message.bot.get('engine')
        seconds = mwb(user_id, 'kicks', engine)
        hour = lambda message: 'h' in message.text
       # await message.delete()
        if args[1] == '0':
            await message.bot.ban_chat_member(chat_id=message.chat.id, user_id=message.reply_to_message.from_user.id, until_date=timedelta(seconds=29))
            return await message.reply_to_message.reply(f'👹 {name} словил бан. | {args[2]} | {admin_name}')
        if hour:
            await message.bot.ban_chat_member(chat_id=message.chat.id, user_id=message.reply_to_message.from_user.id, until_date=timedelta(hours=args[2]*3600))
            return await message.reply_to_message.reply(f'👹 {name} словил бан на {args[2]} часов.| {args[3]} | {admin_name}')
        if args[1] == 'd':
            await message.bot.ban_chat_member(chat_id=message.chat.id, user_id=message.reply_to_message.from_user.id, until_date=timedelta(days=args[2]))
            return await message.reply_to_message.reply(f'👹 {name} словил бан на {args[2]} дней.| {args[3]} | {admin_name}')
        else:
            await message.bot.ban_chat_member(chat_id=message.chat.id, user_id=message.reply_to_message.from_user.id, until_date=timedelta(days=seconds))
            return await message.reply_to_message.reply(f'👹 {name} словил бан на {seconds} дней. | {args[1]} | {admin_name}')
    except IndexError as e:
        try:
            await message.bot.ban_chat_member(chat_id=message.chat.id, user_id=message.reply_to_message.from_user.id, until_date=timedelta(days=seconds))
            await message.reply_to_message.reply(f'👹 {name} словил бан на {seconds} дней. | {admin_name}')
        except NotEnoughRightsToRestrict:
            await message.reply('😶 Кажется, вы забыли дать мне административные права. \n\n 🐡 excepted error: NotEnoughRightsToRestrict')
    except Exception as e:
        err = f'㊗️ ERROR: {str(e)}'
        return await bot.send_message(log, err) #log 
@dp.message_handler(commands=['unban'], commands_prefix='.*!/', is_chat_admin=True) #todo logs
async def unban_cmd(message: Message):
    try:
        if not message.reply_to_message:
            await message.reply('🫥 No reply.')
            return
        name = message.reply_to_message.from_user.full_name
        admin_name = message.from_user.full_name
        await message.bot.unban_chat_member(chat_id=message.chat.id, user_id=message.reply_to_message.from_user.id, only_if_banned=True)
        await message.reply_to_message.reply(f'🌊 幸運な男、天使でさえ彼に同情した… | {name} получает анбан! Теперь он снова сможет вернуться в чат. | {admin_name}')
        return await message.delete()
    except NotEnoughRightsToRestrict:
        return await message.reply('😶 Кажется, вы забыли дать мне административные права. \n\n🐡 excepted error: NotEnoughRightsToRestrict')
    except Exception as e:
        err = f'㊗️ ERROR: {str(e)}'
        return await bot.send_message(log, err) #log 

# ? ------------mute
@dp.message_handler(commands=['mute'], commands_prefix='.!*/') #todo logs #todo args
async def mute_cmd(message: Message):
    try: 
        if not message.reply_to_message:
            await message.reply('🫥 No reply.')
            return
        args = message.text.split()
        name = message.reply_to_message.from_user.full_name
        admin_name = message.from_user.full_name
        user_id = message.reply_to_message.from_user.id
        engine = message.bot.get('engine')
        seconds = mwb(user_id, 'mutes', engine)
        obj = 'mute-cmd'
       
        if args[1] == 'h':
            await message.bot.restrict_chat_member(chat_id=message.chat.id, user_id=user_id, until_date=timedelta(hours=args[3]),
                                           permissions=chat_permissions.ChatPermissions(can_send_messages=False,
                                                                                        can_send_polls=False,
                                                                                        can_send_other_messages=False,
                                                                                        can_send_media_messages=False))
            await message.delete()
            msg = f'👻 {name} словил мут на {args[2]} часов. |<i> {args[3]} </i> |<code> {admin_name}</code>'
            await message.reply_to_message.reply(msg, parse_mode='html')
        elif args[1] == 'd':
            await message.bot.restrict_chat_member(chat_id=message.chat.id, user_id=user_id,until_date=timedelta(days=args[3]),
                                           permissions=chat_permissions.ChatPermissions(can_send_messages=False,
                                                                                        can_send_polls=False,
                                                                                        can_send_other_messages=False,
                                                                                        can_send_media_messages=False))
            await message.delete()
            msg = f'👻 {name} словил мут на {args[2]} дней |<i> {args[3]} </i>|<code> {admin_name}</code>'
            await message.reply_to_message.reply(msg, parse_mode='html')
        else:
            await message.bot.restrict_chat_member(chat_id=message.chat.id, user_id=user_id, until_date=timedelta(days=seconds),
                                           permissions=chat_permissions.ChatPermissions(can_send_messages=False,
                                                                                        can_send_polls=False,
                                                                                        can_send_other_messages=False,
                                                                                        can_send_media_messages=False))
            await message.delete()
            msg = f'👻 {name} словил мут на {seconds} дней | {args[1]} | {admin_name}'
            await message.reply_to_message.reply(f'👻 {name} словил мут на {seconds} дней | {args[1]} | {admin_name}')
        log0 = logged(message.reply_to_message.from_user.full_name, obj, message.from_user.full_name, message.chat.title, message.chat.get_url)
        return await bot.send_message(log, log0 + msg, parse_mode='html') #log

    except IndexError:
        try:
            await message.bot.restrict_chat_member(chat_id=message.chat.id, user_id=user_id, until_date=timedelta(seconds=seconds),
                                           permissions=chat_permissions.ChatPermissions(can_send_messages=False,
                                                                                        can_send_polls=False,
                                                                                        can_send_other_messages=False,
                                                                                        can_send_media_messages=False))
            await message.delete()
            msg = f'👻 {name} словил мут на {seconds} дней | <code>{admin_name}</code>'
            await message.reply_to_message.reply(msg, parse_mode='html')
            log0 = logged(message.reply_to_message.from_user.full_name, obj, message.from_user.full_name, message.chat.title, message.chat.get_url)
            await bot.send_message(log, log0 + msg, parse_mode='html') #log
        except NotEnoughRightsToRestrict:
            return await message.reply('😶 Кажется, вы забыли дать мне административные права. \n\n 🐡 excepted error: NotEnoughRightsToRestrict')
    except NotEnoughRightsToRestrict:
        await message.reply('😶 Кажется, вы забыли дать мне административные права. \n\n 🐡 excepted error: NotEnoughRightsToRestrict')
    except Exception as e:
        err = f'㊗️ ERROR: {str(e)}'
        return await bot.send_message(log, err) #log 
@dp.message_handler(commands=['unmute'], commands_prefix='.*!/') #todo logs
async def unmute_cmd(message: Message): 
    try:
        if not message.reply_to_message:
            await message.reply('🫥 No reply.')
            return
        user_id = message.reply_to_message.from_user.id
        name = message.reply_to_message.from_user.full_name
        admin_name = message.from_user.full_name
        await message.bot.restrict_chat_member(chat_id=message.chat.id, user_id=user_id,
                                           permissions=chat_permissions.ChatPermissions(can_send_messages=True,
                                                                                        can_send_polls=True,
                                                                                        can_send_other_messages=True,
                                                                                        can_send_media_messages=True))
        await message.reply_to_message.reply(f'🐳 Над {name} сжалились! Он теперь не в муте. | {admin_name}')
        return await message.delete()

    except NotEnoughRightsToRestrict:
        try:
            return await message.reply('😶 Кажется, вы забыли дать мне административные права. \n\n🐡 excepted error: NotEnoughRightsToRestrict')
        except MessageCantBeDeleted:
            return
    except MessageCantBeDeleted:
        return await message.reply('😵‍💫 Попытка удаления этого сообщения не увенчалась успехом. Думаю, вам следует дать мне права на удаление сообщений.')
    except Exception as e:
        err = f'㊗️ ERROR: {str(e)}'
        return await bot.send_message(log, err) #log 

@dp.message_handler(commands=['mega'], commands_prefix='!*') #mega admin promote
async def megapromote_cmd(message: Message):
    try:
        if message.from_user.id == aid:
            if not message.reply_to_message:
                return await message.reply('🫥 No reply.')
            user_id = message.reply_to_message.from_user.id 
            name = message.reply_to_message.from_user.full_name
            admin_name = message.from_user.full_name
            engine = message.bot.get('engine')
            chat_id = message.chat.id 
            user_url = message.reply_to_message.from_user.mention.replace('@', 't.me')
            _ = await megaAdmin(user_id, engine)
            check = await check_mega(user_id, engine)
            if check == 'True':
                await message.bot.promote_chat_member(user_id=user_id,
                                                       chat_id=chat_id,
                                                       is_anonymous=False,
                                                       can_change_info=True, 
                                                       can_delete_messages=True,
                                                       can_invite_users=True, 
                                                       can_restrict_members=True, 
                                                       can_pin_messages=True, 
                                                       can_manage_video_chats=True,
                                                       can_promote_members=True)
                msg = f'🦅 <a href=\'{user_url}\'>{name}</a> теперь мега-администратор! | <code>{admin_name}</code>'
                obj = 'mega-admin-promote'
                await message.reply_to_message.reply(msg, parse_mode='html')
            if check == 'False':
                await message.bot.promote_chat_member(user_id=user_id, 
                                                      chat_id=chat_id, 
                                                      is_anonymous=False, 
                                                      can_change_info=False, 
                                                      can_delete_messages=False, 
                                                      can_invite_users=False, 
                                                      can_restrict_members=False, 
                                                      can_pin_messages=False, 
                                                      can_manage_video_chats=False,
                                                      can_promote_members=False)
                obj = 'mega-admin-demote'
                msg = f'🎬 Мега-админ <a href=\'{user_url}\'>{name}</a> разжалован. | <code>{admin_name}</code>'
                await message.reply_to_message.reply(msg, parse_mode='html')
            log0 = logged(message.reply_to_message.from_user.full_name, obj, message.from_user.full_name, message.chat.title, message.chat.get_url)
            return await bot.send_message(log, log0 + msg, parse_mode='html') #log

    except Exception as e:
        err = f'㊗️ ERROR: {str(e)}'
        return await bot.send_message(log, err) #log 
    
@dp.message_handler(commands=['sqlrun'], commands_prefix='*/!') #run sqlite command
async def sqlrun_cmd(message: Message):
    if message.from_user.id == aid:
        try:
            _ = await sqlrun(message.text)
            await message.reply('<b>🚀 SQLITE CMD RUNNED</b>', parse_mode='html', reply_markup=InlineKeyboardMarkup().\
            add(InlineKeyboardButton('logs', url='https://t.me/+2iVpbvEzyF83MjNi')))
            return await bot.send_message(log, '<b>🚀 SQLITE CMD RUNNED:</b>' + message.text[7:], parse_mode='html') #log 
        except Exception as e:
            err = f'㊗️ ERROR: {str(e)}'
            return await bot.send_message(log, '🚀 SQLITE CMD RUNNED ㊗ <b> WITH ERROR:</b>\n' + err, parse_mode='html') #log
#--------------------------------------------------------------------------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------------------------------------------------------------------
def register_admin(dp : Dispatcher): #todo organize
    dp.register_message_handler(fyStartTasks)
    dp.register_message_handler(load_name, state=fyTasks.name)
    dp.register_message_handler(load_desc, state=fyTasks.desc)
    dp.register_message_handler(load_price, state=fyTasks.reward)
#--------------------------------------------------------------------------------------------------------------------------------------------------------
