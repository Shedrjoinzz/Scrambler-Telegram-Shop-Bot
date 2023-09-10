from aiogram import types

from datetime import datetime

from loader import dp
from data.db import DB
from keyboards import inline_keyboards as ikb

@dp.callback_query_handler(text='faq_')
async def call_faq(call: types.CallbackQuery):
    with DB() as db:
        get_faq_shop = db.give_faq_shop()

    date_time_str = str(datetime.now()).split(".")[0]
    await call.message.edit_text(f'{get_faq_shop[0]}'.replace("%first_name%", f"{call.from_user.first_name}").replace("%username%", f"{call.from_user.username}").replace("%user_id%", f"{call.from_user.id}").replace("%datetime%", f"{date_time_str}"),
                                 reply_markup=ikb.back_basket_list('back_menu'))