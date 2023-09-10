from aiogram import types

from loader import dp
from keyboards import inline_keyboards as ikb

@dp.callback_query_handler(text='management_users_admin_')
async def call_management_users_admin(call: types.CallbackQuery):
    await call.message.edit_text('Выберите раздел', reply_markup=ikb.select_users_manager())