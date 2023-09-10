import aiogram
from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.storage import FSMContext

import asyncio

from loader import dp, bot
from data.db import DB
from libs.config import id_admin
from states.state import EditUserInfo

@dp.callback_query_handler(Text(startswith='add_in_admin_id'), state=EditUserInfo.id_user)
async def call_add_in_admin_id(call: types.CallbackQuery, state: FSMContext):
    id_user = int(call.data.split('_')[4])
    list_admins = id_admin()

    message_text = ''
    if list_admins[0] == call.message.chat.id:

        if not id_user in list_admins:

            with DB() as db:
                info_user = db.give_info_user('name, lastname', id_user)
                full_name = f'{info_user[0]} {info_user[1]}'
                db.add_new_admin(id_user, full_name, 0)

            try:
                await bot.send_message(id_user, '<b>Вас назначили Администратором Магазина, пожалуйста, отправьте команду /start что-бы обновить данные</b>')

            except:
                message_text = '<i>Не получилось оповестить пользоватля назначением его в Админы</i>'
                return

            message_text = f'<b>Пользователь <code>{id_user}</code> теперь Администратор!</b>'
            
            # await state.finish()
        
        else:
            message_text = '<b>Пользователь и так Администратор\nЧто-бы управлять Админами перейдите в раздел Админка -> Админы</b>'

    else:
        message_text = '<b>У вас нет уполномочий назначать пользователей Админами</b>'
    
    _id_msg = await call.message.answer(message_text)
    await asyncio.sleep(5)
    try:
        await bot.delete_message(call.message.chat.id, message_id=_id_msg.message_id)
    except aiogram.utils.exceptions.MessageToDeleteNotFound:
        pass