from aiogram import types
import aiogram

import asyncio

from keyboards import inline_keyboards as ikb
from data.db import DB
from loader import dp, bot
from libs.config import id_admin

@dp.callback_query_handler(text='ban_all_users')
async def call_ban_all_users(call: types.CallbackQuery):
    await call.message.edit_text('Данное действие Заблокирует всех пользователей\n\n<b>-Не касается Админов</b>', reply_markup=ikb.confirm_the_ban_all_users())


@dp.callback_query_handler(text='confirm_all_ban_users')
async def call_confirm_all_ban_users(call: types.CallbackQuery):

    with DB() as db:
        get_all_users = db.get_count_users_in_spam()
        get_all_admins = id_admin()

        
        msg_is_ban_users = '<b>Все пользователи были заблокированы!</b>'
        for id_users in get_all_users:
            if id_users[0] not in get_all_admins:

                user_is_ban = db.give_ban_info_user(id_users[0])
                if user_is_ban is None:
                    db.update_ban_list('ban', id_users[0], '-')

                if user_is_ban is not None:
                    msg_is_ban_users += '\n\n[?] Некоторые пользователи уже были заблокированы'

        _id = await call.message.answer(msg_is_ban_users)
        await asyncio.sleep(5)
        try:
            await bot.delete_message(call.message.chat.id, message_id=_id.message_id)
        except aiogram.utils.exceptions.MessageToDeleteNotFound:
            pass