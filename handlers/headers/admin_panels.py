import aiogram
from aiogram import types
from aiogram.dispatcher.filters import Text

from libs.config import id_admin
from keyboards import admin_keyboards as aikb
from loader import dp

@dp.callback_query_handler(text='admin_')
async def call_admin_panel(call: types.CallbackQuery):
    try:
        if call.message.chat.id not in id_admin():
            return await call.message.edit_text('Вы больше не админ!', reply_markup=None)
        elif call.message.chat.id in id_admin():
            await call.message.edit_text('Админ панель', reply_markup=aikb.main_admin_panel())
    except aiogram.utils.exceptions.MessageNotModified:
        pass
    except aiogram.utils.exceptions.MessageToEditNotFound:
        pass

@dp.callback_query_handler(Text(startswith='close_state_in_delete_catalog_'))
async def  call_close_state_in_delete_catalog(call: types.CallbackQuery):
    try:
        if call.message.chat.id not in id_admin():
            return await call.message.edit_text('Вы больше не админ!', reply_markup=None)
        elif call.message.chat.id in id_admin():
            await call.message.edit_text('Админ панель', reply_markup=aikb.main_admin_panel())
    except aiogram.utils.exceptions.MessageNotModified:
        pass
    except aiogram.utils.exceptions.MessageToEditNotFound:
        pass