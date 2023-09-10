from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext

from keyboards import inline_keyboards as ikb
from keyboards import admin_keyboards as aikb
from states.state import EditProductOne
from data.db import DB
from loader import dp
from handlers import commands as com


@dp.callback_query_handler(Text(startswith='edit_old_product_'))
async def call_edit_old_product(call: types.CallbackQuery):
    with DB() as db:
        req = db.give_all_catalogs()

    if [] == req:
        await call.message.edit_text('Для изменения товара в каталог вам необходимо сначала создать каталог', reply_markup=ikb.multi_control_category(req, db, 'edit', 'product'))
        return

    await call.message.edit_text('Выберите каталог в котором хотите изменить товар', reply_markup=ikb.multi_control_category(req, db, 'edit', 'product'))


@dp.callback_query_handler(Text(startswith='edit_product_'))
async def call_edit_product(call: types.CallbackQuery):
    call_msg = call.data.split('_')
    
    with DB() as db:
        req = db.give_all_product_in_catalogs(call_msg[2])

    await call.message.edit_text('Выберите товар который хотите изменить', reply_markup=ikb.give_product_in_catalog('edits_', call_msg[2], req))

@dp.callback_query_handler(Text(startswith='edits_product_'))
async def call_edits_product(call: types.CallbackQuery):
    call_msg = call.data.split('_')

    with DB() as db:
        req = db.give_info_product(call_msg[2])

    for i in req:
        await call.message.edit_text(f'<b>1) Название товара:</b> <code>{i[2]}</code>\n\n'
                                     f'<b>2) Описание товара:</b> <code>{i[3]}</code>\n\n'
                                     f'<b>3) Стоимость товара:</b> <code>{i[4]}</code> <b>RUB</b>\n\n'
                                     f'<b>4) Количество товара:</b> <code>{i[5]}</code>\n\n'
                                     f'<b>5) Ссылка на товар:</b> <code>{i[6]}</code>\n\n'
                                     'Выберите что хотите изменить 👇', reply_markup=ikb.select_edit_element_in_product(i[0]))

@dp.callback_query_handler(Text(startswith='one_old_edit_product_'))
async def call_manager_bot_edit(call: types.CallbackQuery, state: FSMContext):
    call_msg = int(call.data.split('_')[4])
    call_msg_id_product = int(call.data.split('_')[5])

    await state.set_state(EditProductOne.id_product)

    async with state.proxy() as data:
        data['id_product'] = call_msg_id_product
        data['id_call_msg'] = call_msg
    
    if call_msg == 1:
        await call.message.edit_text('<b>Пришлите новое название товара не более 64 символов:</b>', reply_markup=ikb.cancel_edit_one_product())
    
    if call_msg == 2:
        await call.message.edit_text('<b>Пришлите новое краткое описание товара не более 600 символов:</b>', reply_markup=ikb.cancel_edit_one_product())

    if call_msg == 3:
        await call.message.edit_text('<b>Пришлите новую стоимость товара:</b>', reply_markup=ikb.cancel_edit_one_product())

    if call_msg == 4:
        await call.message.edit_text('<b>Пришлите новое количество товара:</b>', reply_markup=ikb.cancel_edit_one_product())
        
    if call_msg == 5:
        await call.message.edit_text('<b>Пришлите новую ссылку на товар который выдадут после его приобретения:</b>', reply_markup=ikb.cancel_edit_one_product())
    
        
@dp.message_handler(state=EditProductOne.id_product)
async def set_characteristic(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        get_id_product = data['id_product']
        get_id_call_msg = data['id_call_msg']

    with DB() as db:
        
        if get_id_call_msg == 1:

            if len(message.text) > 64:
                await message.answer(f'Максимум 64 символов в названии товара, в вашем {len(message.text)} символов:', reply_markup=ikb.cancel_edit_one_product())
                return

            db.update_products('str', 'name_product', message.text, get_id_product)
            await message.answer(f'<b>Название товара успешно изменено на:</b> <code>{message.text}</code>', reply_markup=aikb.main_admin_panel())

        if get_id_call_msg == 2:

            if len(message.text) > 600:
                await message.answer(f'Максимум 600 символов в описании товара, в вашем {len(message.text)} символов:', reply_markup=ikb.cancel_edit_one_product())
                return
            
            db.update_products('str', 'description_product', message.text, get_id_product)
            await message.answer(f'<b>Описание товара успешно изменено на:</b> <code>{message.text}</code>', reply_markup=aikb.main_admin_panel())
            
        if get_id_call_msg == 3:

            try:
                int_new_price = int(message.text)

                if int_new_price > 1_000_000:
                    await message.answer('<b>Слишком дорогой товар, максимум 1 000 000 RUB</b>', reply_markup=ikb.cancel_edit_one_product())
                    return
                
                db.update_products('int', 'price', message.text, get_id_product)
                await message.answer(f'<b>Стоимость товара успешно изменено на:</b> <code>{message.text} RUB</code>', reply_markup=aikb.main_admin_panel())
                
            except ValueError:
                await message.answer('<b>Введите число!</b>', reply_markup=ikb.cancel_edit_one_product())
                return

        
        if get_id_call_msg == 4:
            try:
                int_new_count = int(message.text)

                if int_new_count > 10_000:
                    await message.answer('<b>Слишком огромное количество товара, максимум 10 000</b>', reply_markup=ikb.cancel_edit_one_product())
                    return
                
                db.update_products('int', 'count_products', message.text, get_id_product)
                await message.answer(f'<b>Количество товара успешно изменено на:</b> <code>{message.text}</code>', reply_markup=aikb.main_admin_panel())

            except ValueError:
                await message.answer('<b>Введите число!</b>', reply_markup=ikb.cancel_edit_one_product())
                return

        if get_id_call_msg == 5:
            if len(message.text) > 600:
                await message.answer('<b>Слишком длинная ссылка</b>', reply_markup=ikb.cancel_edit_one_product())
                return
            
            if not 'https://' in message.text:
                await message.reply('<b>Не видно ссылки на товар "https://"</b>', reply_markup=ikb.cancel_edit_one_product())
                return
            
            db.update_products('str', 'link_products', message.text, get_id_product)
            await message.answer(f'<b>Ссылка на товар успешно изменено на:</b> <code>{message.text}</code>', reply_markup=aikb.main_admin_panel())
        
        await state.finish()
        await com.delete_all_message_chat(message)
