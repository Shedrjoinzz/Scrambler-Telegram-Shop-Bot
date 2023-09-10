from aiogram.types import CallbackQuery

from loader import dp
from data.db import DB
from handlers import user_panel as ikb
from handlers import commands as com

@dp.callback_query_handler(text='back_menu')
async def retring(call: CallbackQuery):
    with DB() as db:
        id_user = db.give_id_user(call.from_user.id)
        get_start_message = db.give_message_is_start_and_message_is_buy_and_status_bot_and_captcha()
    if id_user == None:
        db.add_new_user(call.from_user.id, 0, 0, call.from_user.first_name, call.from_user.last_name, call.from_user.username, call.from_user.language_code)
        if get_start_message[2] != '-':
            await call.message.edit_text(f'{get_start_message[2]}'.replace("%first_name%", call.from_user.first_name).replace("%username%", call.from_user.username).replace("%user_id%", f"{call.from_user.id}"))
            return

        await call.message.answer('Добро пожаловать!', reply_markup=ikb.user_panel(call.message.chat.id))

    if get_start_message[0] != '-':
        await call.message.edit_text(f'{get_start_message[0]}'.replace("%first_name%", call.from_user.first_name).replace("%username%", call.from_user.username).replace("%user_id%", f"{call.from_user.id}"),
                                reply_markup=ikb.user_panel(call.message.chat.id))
        return

    await call.message.edit_text('Главное меню', reply_markup=ikb.user_panel(call.message.chat.id))
    # await com.delete_all_message_chat(call.message)
    # await call.message.delete()

@dp.callback_query_handler(text='close_admin_panel_')
async def call_close_admin_panel_(call: CallbackQuery):
    await call.message.delete()
    await com.delete_all_message_chat(call.message)
    await call.message.answer('Админка закрыта', reply_markup=ikb.user_panel(call.message.chat.id))
