from aiogram import types
from aiogram.dispatcher.storage import FSMContext

from handlers import commands as com
from loader import dp
from data.db import DB
from keyboards import inline_keyboards as ikb
from states.state import EditProcentAllUsers


@dp.callback_query_handler(text='edit_procent_all_users')
async def call_edit_procent_user(call: types.CallbackQuery, state: FSMContext):
    await state.set_state(EditProcentAllUsers.procent)
    await call.message.edit_text('Отправьте процент который хотите Установить ВСЕМ пользователям от 0 до 100', reply_markup=ikb.cancel_edit_all_users_procent())


@dp.message_handler(state=EditProcentAllUsers.procent)
async def edit_all_users_procent(message: types.Message, state: FSMContext):
    await com.delete_all_message_chat(message)
    
    try:
        _float_procent = float(message.text)

    except ValueError:
        await message.answer('Отправьте процент от 0 до 100:', reply_markup=ikb.cancel_edit_all_users_procent())
        return
    
    if _float_procent > 100:
        await message.answer('<b>Максимум процент 100!</b>', reply_markup=ikb.cancel_edit_all_users_procent())
        return
    
    if _float_procent < 0:
        await message.answer('<b>Минимум процент 0!</b>', reply_markup=ikb.cancel_edit_all_users_procent())
        return
    
    with DB() as db:
        db.edit_all_procent(_float_procent)

    await state.finish()
    await message.answer(f'Всем пользователям был установлен <b>{_float_procent}%</b>', reply_markup=ikb.back_excel_data())




