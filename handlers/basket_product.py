from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext

from keyboards import inline_keyboards as ikb
from states.state import CountBasketProduct
from data.db import DB
from loader import dp
from . import commands as com

@dp.callback_query_handler(Text(startswith='basket_'))
async def call_buy_products(call: types.CallbackQuery):
    call_msg = call.data.split('_')
    with DB() as db:
        get_ban_list = db.give_is_ban_users(call.message.chat.id)
        if get_ban_list:
            get_info_ban = db.give_ban_info_user(call.message.chat.id)
            await call.message.edit_text(f'<b>Вы были заблокированы!\n\nПричина:</b> <i>{get_info_ban[1]}</i>')
            return
        
        if call_msg[3] != 'edit':
            get_id_products = db.give_info_product(call_msg[1])

            db.add_products_in_basket(call.message.chat.id, get_id_products[0][0], get_id_products[0][1], call_msg[2])
        else:
            db.edit_count_products_in_basket(call.message.chat.id, call_msg[1], call_msg[2])
            return await call.message.edit_text('Товар успешно был изменён', reply_markup=ikb.back_basket_list('basketgiveproducts_'))
        
    if get_id_products[0][5] > 0:
        await call.message.edit_text('<b>Товар успешно добавлен в корзину</b>', reply_markup=ikb.back_list_catalog())
    else:
        await call.message.edit_text('<b>Товар НЕ был добавлен в корзину, возможно купили последний :(</b>', reply_markup=ikb.back_list_catalog())

@dp.callback_query_handler(Text(startswith='basketgiveproducts_'))
async def call_give_products(call: types.CallbackQuery):
    with DB() as db:
        get_basket = db.give_basket_products_all(call.message.chat.id)
    if get_basket != []:
        # print(len(get_basket))
        await call.message.edit_text('<b>Ваша корзина</b>', reply_markup=ikb.give_basket_products(get_basket, db))
        await com.delete_all_message_chat(call.message)
    else:
        await call.message.edit_text('<b>Тут пусто :(</b>\n\n'
                                     '<i>Для отображения товаров в корзине, перейдите в каталог и добавьте пару товаров в корзину</i>', reply_markup=ikb.back_basket_list('back_menu'))

@dp.callback_query_handler(Text(startswith='EditBasketProduct_'))
async def call_edit_basket_product(call: types.CallbackQuery, state: FSMContext):
    data_msg = call.data.split('_')
    await state.set_state(CountBasketProduct.count_product)
    
    if data_msg[1] != 'cancel':
        async with state.proxy() as data:
            data['id_product'] = data_msg[2]
            data['max_count'] = data_msg[5]

        await call.message.edit_text(f'Изменение количества товара <b>{data_msg[3]}</b>\n'
                                     f'Всего в базе: <b>{data_msg[5]}</b>\n\n'
                                     f'Отправьте кол-во товаров для изменения вашего текущего <b>{data_msg[4]}</b> кол-во товаров или выберите допустимый из кнопок ниже.', reply_markup=ikb.multi_give_count('edit', data_msg[5]))
    else:
        await call.message.edit_text(f'Отмена добавления товара в корзину', reply_markup=ikb.back_list_catalog())

@dp.message_handler(state=CountBasketProduct.count_product)
async def end_edit_count_product_in_basket(message: types.Message, state: FSMContext):
    await state.update_data(count_product=message.text.lower())
    try:
        async with state.proxy() as data:
            _id_product = data['id_product']
            _max_count = int(data['max_count'])
            _count_product = int(data['count_product'])
        
        if _count_product <= 0:
            await message.answer('Нельзя изменить на меньше чем 1-го товара!')

        elif _count_product <= _max_count:
            await message.answer(f'Выбрано <b>{_count_product}</b> товаров\n'
                                 'Нажмите <b>Готово</b>, чтобы сохранить изменения в корзине', reply_markup=ikb.edit_basket_count(_id_product, _count_product, 'edit'))
            await com.delete_all_message_chat(message)
            await state.finish()

        else:
            await message.answer(f'Нельзя указывать больше {_max_count} товаров.')
    except ValueError:
        await message.answer('Вы должны указать цифру!')
    

@dp.callback_query_handler(Text(startswith='pressEditCount_'), state=CountBasketProduct.count_product)
async def call_pressCount(call: types.CallbackQuery, state: FSMContext):
    call_msg = call.data.split('_')
    await state.update_data(count_product=call_msg[1])

    async with state.proxy() as data:
        _id_product = data['id_product']
        _max_count = int(data['max_count'])
        _count_product = int(data['count_product'])


    if _count_product <= _max_count:
        await call.message.edit_text(f'Выбрано <b>{_count_product}</b> товаров\n'
                                    'Нажмите <b>Готово</b>, чтобы изменить корзину', reply_markup=ikb.edit_basket_count(_id_product, _count_product, 'edit'))
        await com.delete_all_message_chat(call.message)
        await state.finish()

