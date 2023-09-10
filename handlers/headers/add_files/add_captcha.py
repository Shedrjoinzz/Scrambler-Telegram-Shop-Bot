import aiogram
from aiogram import types
from aiogram.dispatcher.filters import Text

import asyncio

from data.db import DB
from loader import dp, bot


@dp.callback_query_handler(Text(startswith='add_captcha_'))
async def call_select_number(call: types.CallbackQuery):
    call_msg = call.data.split('_')

    with DB() as db:
        db.update_captcha_in_manager_bot(call_msg[2])
    
    user_msg = '<b>Установлен Режим Защиты:</b> '

    if call_msg[2] == '1':
        user_msg += '<code>Выбор Цифры</code>'
    
    if call_msg[2] == '2':
        user_msg += '<code>Ввод Цифр</code>'

    if call_msg[2] == '3':
        user_msg += '<code>Решение Уровнений</code>'
    
    if call_msg[2] == '0':
        user_msg = '<b>Капча:</b> <code>Отключена</code>'
    
    _id = await call.message.answer(user_msg)

    await asyncio.sleep(2)
    try:
        await bot.delete_message(call.message.chat.id, message_id=call.message.message_id)
    except aiogram.utils.exceptions.MessageToDeleteNotFound:
        pass
