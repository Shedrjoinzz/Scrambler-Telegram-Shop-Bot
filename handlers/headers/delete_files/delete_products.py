from aiogram import types
from aiogram.dispatcher.filters import Text

from data.db import DB
from loader import dp
from keyboards import inline_keyboards as ikb
from keyboards.inline_keyboards import back_basket_list

@dp.callback_query_handler(Text(startswith='delete_products_'))
async def call_delete_products(call: types.CallbackQuery):
    call_msg = call.data.split('_')
    with DB() as db:
        req = db.give_all_catalogs()

    if req != []:
        await call.message.edit_text('Выберите каталог в котором хотите удалить товар', reply_markup=ikb.multi_control_category(req, db, 'delgive', 'delete_product'))
    else:
        await call.message.edit_text('<b>Товары отсутствуют</b>\n\n-Для удаления товара из каталога вам необходимо сначала создать каталог и заполнить его товарами', reply_markup=ikb.multi_control_category(req, db, 'add', 'product'))

@dp.callback_query_handler(Text(startswith='delgive_product_'))
async def call_delete_product(call: types.CallbackQuery):
    call_msg = call.data.split('_')
    with DB() as db:
        req = db.give_all_product_in_catalogs(call_msg[2])
    if req != []:
        await call.message.edit_text('Выберите товар который хотите удалить', reply_markup=ikb.give_product_in_catalog('delete_', call_msg[2], req))
    else:
        await call.message.edit_text('Товаров в каталоге больше нет', reply_markup=ikb.give_product_in_catalog('delete_', call_msg[2], req))

@dp.callback_query_handler(Text(startswith='delete_product_'))
async def call_deletemethod(call: types.CallbackQuery):
    call_msg = call.data.split('_')
    with DB() as db:
        db.delete_from_products(call_msg[2])
        req = db.give_all_product_in_catalogs(call_msg[3])
    if req != []:
        await call.message.edit_text('<b>Товар удалён с каталога</b>\n\nВыберите товар который хотите удалить', reply_markup=ikb.give_product_in_catalog('delete_', call_msg[2], req))
    else:
        await call.message.edit_text('<b>Товар удалён с каталога</b>\n\nТоваров в каталоге больше нет', reply_markup=ikb.give_product_in_catalog('delete_', call_msg[2], req))

@dp.callback_query_handler(Text(startswith='DelBasketProduct_'))
async def call_delete_basket_prducts(call: types.CallbackQuery):
    call_msg = call.data.split('_')
    with DB() as db:
        db.delete_product_in_basket(call.message.chat.id, call_msg[2])
    await call.message.edit_text(f'Товар {call_msg[3]} успешно удален из корзины!', reply_markup=back_basket_list('basketgiveproducts_'))

@dp.callback_query_handler(Text(startswith='delete_all_product_'))
async def call_delete_all_product(call: types.CallbackQuery):
    call_msg = call.data.split('_')

    with DB() as db:
        db.delete_all_products_from_catalog(call_msg[3])
        req = db.give_all_product_in_catalogs(call_msg[3])
    await call.message.edit_text('<b>Все товары были удалены с каталога</b>\n\nТоваров в каталоге больше нет', reply_markup=ikb.give_product_in_catalog('delete_', call_msg[3], req))