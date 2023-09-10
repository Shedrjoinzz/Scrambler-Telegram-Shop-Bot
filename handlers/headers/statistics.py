from aiogram import types

from loader import dp
from data.db import DB
from keyboards import inline_keyboards as ikb

@dp.callback_query_handler(text='statistic_admin_')
async def call_statistic_admin(call: types.CallbackQuery):
    with DB() as db:
        get_count_users = db.give_count_users()
        get_count_ban_users = db.give_count_ban_users()
        get_money = db.give_money_admin()
        get_user_ref = db.give_count_all_ref_users()
        get_user_not_ref = db.give_count_all_not_ref_users()

    await call.message.edit_text('<b>Статистика Бота</b>\n\n'
                                f'Пользователей: {get_count_users[0][0]}\n'
                                f'Перешли по реф.ссылке: {get_user_ref[0][0]}\n'
                                f'Пришли сами: {get_user_not_ref[0][0]}\n'
                                f'Пользователей в бане: {get_count_ban_users[0][0]}\n'
                                f'Заработано: {get_money[0]} RUB', reply_markup=ikb.back_in_admin_menu())