import aiogram
from aiogram import types

import asyncio

from loader import dp, bot
from keyboards import inline_keyboards as ikb
from data.db import DB


@dp.callback_query_handler(text='unban_all_users')
async def call_unban_all_users(call: types.CallbackQuery):

    await call.message.edit_text('<b>Вы уверены что хотите разблокировать всех пользователей бота?</b>\n'
                                 '[?] Так-же разблокируются нежелательные пользователи', reply_markup=ikb.confirm_the_unban_all_users())
    

@dp.callback_query_handler(text='confirm_all_unban_users')
async def call_confirm_all_ban_users(call: types.CallbackQuery):

    message_delete_all_users = ""
    with DB() as db:
        get_ban_list_users = db.give_is_not_None_ban_list()
        if [] == get_ban_list_users:
            message_delete_all_users = "<b>Больше нет Заблокированных пользователей!</b>"

        if [] != get_ban_list_users:
            message_delete_all_users = "<b>Все пользователи были Разблокированы!</b>"        
            db.unlock_all_users()

    _id = await call.message.answer(message_delete_all_users)
    await asyncio.sleep(5)
    try:
        await bot.delete_message(call.message.chat.id, message_id=_id.message_id)
    except aiogram.utils.exceptions.MessageToDeleteNotFound:
        pass