from aiogram import types

from loader import dp
from data.db import DB

@dp.message_handler()
async def check_ban_user(message: types.Message):
    with DB() as db:
        get_ban_list = db.give_is_ban_users(message.chat.id)
        if get_ban_list:
            get_info_ban = db.give_ban_info_user(message.chat.id)
            await message.answer(f'<b>Вы были заблокированы!\n\nПричина:</b> <i>{get_info_ban[1]}</i>')
            return


