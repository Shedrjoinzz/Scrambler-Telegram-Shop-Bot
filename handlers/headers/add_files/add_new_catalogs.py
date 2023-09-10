import aiogram
from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext

from keyboards import inline_keyboards as ikb
from keyboards import admin_keyboards as aikb
from states.state import AddCatalogs
from data.db import DB
from loader import dp, bot
from handlers import commands as com

@dp.callback_query_handler(Text(startswith='add_catalogs_'))
async def call_add_catalogs_(call: types.CallbackQuery, state: FSMContext):
    await state.set_state(AddCatalogs.name_catalog)
    with DB() as db:
        get_all_name_catalogs = db.give_all_catalogs()
    
    async with state.proxy() as data:
        data['old_name_catalog'] = get_all_name_catalogs

    await call.message.edit_text('<b>Введите название каталога:</b>', reply_markup=ikb.success_button('0'))


@dp.message_handler(state=AddCatalogs.name_catalog)
async def handler_end_add_count_in_basket_products(message: types.Message, state: FSMContext):
    await state.update_data(name_catalog=message.text)
    
    async with state.proxy() as data:
        _old_name_catalog = data['old_name_catalog']
        _name_catalog = data['name_catalog']

    for i in _old_name_catalog:
        if i[1] == _name_catalog:
            await message.reply(f'У вас уже имеется каталог c таким названием {i[1]}, если хотите добавить каталог с таким же названием <b>{_name_catalog}</b> то нажмите <b>Сохранить</b> или пришлите новое название:', reply_markup=ikb.success_button('1'))
        else:
            await message.reply(f'Нажмите сохранить что бы создать каталог <b>{_name_catalog}</b>, или пришлите новое название:', reply_markup=ikb.success_button('1'))
        return
    else:
        await message.reply(f'Нажмите сохранить что бы создать каталог <b>{_name_catalog}</b>, или пришлите новое название:', reply_markup=ikb.success_button('1'))



@dp.callback_query_handler(Text(startswith='add_success_'), state=AddCatalogs.name_catalog)
async def call_success_add(call: types.CallbackQuery, state: FSMContext):
    call_msg = call.data.split('_')
    if call_msg[2] == '1':
        await com.delete_all_message_chat(call.message)
        async with state.proxy() as data:
            with DB() as db:
                db.add_catalog(data['name_catalog'])
        try:
            await bot.delete_message(call.message.chat.id, message_id=call.message.message_id)
        except aiogram.utils.exceptions.MessageToDeleteNotFound:
            pass
        await call.message.answer('Каталог успешно добавлен!', reply_markup=aikb.main_admin_panel())
        await state.finish()

@dp.callback_query_handler(text='add_catalog_cancel', state=AddCatalogs.name_catalog)
async def call_cancel_state(call: types.CallbackQuery, state: FSMContext):
    call_msg = call.data.split('_')
    print(call_msg)
    if call_msg[1] == '1' or '0':
        await call.message.edit_text(f'Отмена добавления каталога', reply_markup=aikb.main_admin_panel())
        await state.finish()
        await com.delete_all_message_chat(call.message)