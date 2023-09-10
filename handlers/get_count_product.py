from aiogram.dispatcher import FSMContext
from aiogram import types
from aiogram.dispatcher.filters import Text

from loader import dp
from states.state import CountAddBasketProduct
from data.db import DB
from keyboards import inline_keyboards as ikb
from . import commands as com


@dp.callback_query_handler(Text(startswith='CountInBasket_'))
async def call_add_count_product_in_basket(call: types.CallbackQuery, state: FSMContext):
    data_msg = call.data.split('_')
    await state.set_state(CountAddBasketProduct.count_product)
    if data_msg[1] != 'cancel':
        with DB() as db:
            count_products = db.select_method_products('count_products', data_msg[2])
            isProduct = db.check_basket_product(call.message.chat.id, data_msg[2])
            if isProduct:
                return await call.message.edit_text('Товар уже добавлен в корзину. Хотите увеличить количество товара?')
        async with state.proxy() as data:
            data['id_product'] = data_msg[2]
            data['max_count'] = count_products[0]

        await call.message.edit_text(f'Отправьте количество товаров\n\n<i>максимум товаров в базе {count_products[0]}</i>', reply_markup=ikb.multi_give_count('add', count_products[0]))
    else:
        await call.message.edit_text(f'Отмена добавления товара в корзину', reply_markup=ikb.back_list_catalog())


@dp.message_handler(state=CountAddBasketProduct.count_product)
async def handler_end_add_count_in_basket_products(message: types.Message, state: FSMContext):
    await state.update_data(count_product=message.text.lower())
    try:
        async with state.proxy() as data:
            _id_product = data['id_product']
            _max_count = int(data['max_count'])
            _count_product = int(data['count_product'])
        
        if _count_product <= 0:
            await message.answer('Нельзя добавить меньше 1 товара!')

        elif _count_product <= _max_count:
            await message.answer(f'Выбрано <b>{_count_product}</b> товаров\n'
                                 'Нажмите <b>Готово</b>, чтобы добавить в корзину', reply_markup=ikb.add_basket_count(_id_product, _count_product, 'noEdit'))
            await com.delete_all_message_chat(message)
            await state.finish()

        else:
            await message.answer(f'Нельзя указать больше {_max_count} товаров.')
    except ValueError:
        await message.answer('Вы должны указать цифру!')


@dp.callback_query_handler(Text(startswith='pressCount_'), state=CountAddBasketProduct.count_product)
async def call_pressCount(call: types.CallbackQuery, state: FSMContext):
    call_msg = call.data.split('_')
    await state.update_data(count_product=call_msg[1])
    async with state.proxy() as data:
        _id_product = data['id_product']
        _max_count = int(data['max_count'])
        _count_product = int(data['count_product'])
    
    if _count_product <= _max_count:
        await call.message.edit_text(f'Выбрано <b>{_count_product}</b> товаров\n'
                                    'Нажмите <b>Готово</b>, чтобы добавить в корзину', reply_markup=ikb.add_basket_count(_id_product, _count_product, 'noEdit'))
        await com.delete_all_message_chat(call.message)
        await state.finish()

