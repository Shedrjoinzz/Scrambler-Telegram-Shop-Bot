from aiogram.types import CallbackQuery
from aiogram.dispatcher.filters import Text

from loader import dp
from data.db import DB
from keyboards import inline_keyboards as ikb


@dp.callback_query_handler(text='catalog_s')
async def call_get_all_catalogs(call: CallbackQuery):
    with DB() as db:
        get_ban_list = db.give_is_ban_users(call.message.chat.id)
        if get_ban_list:
            get_info_ban = db.give_ban_info_user(call.message.chat.id)
            await call.message.edit_text(f'<b>Вы были заблокированы!\n\nПричина:</b> <i>{get_info_ban[1]}</i>')
            return
        
        req = db.give_all_catalogs()
    if [] != req:
        await call.message.edit_text('Каталоги', reply_markup=ikb.give_category(req, db))
    else:
        await call.message.edit_text('Каталоги отсутствуют', reply_markup=ikb.give_category(req, db))

@dp.callback_query_handler(Text(startswith='catalog_'))
async def call_press_catalog_id(call: CallbackQuery):
    msg = call.data.split('_') # get all product in id catalog

    if msg[1] != '':
        with DB() as db:
            req = db.give_all_product_in_catalogs(msg[1])

            select_name_catalog = db.give_name_catalogs(msg[1])
    if [] != req:
        await call.message.edit_text(f'<b>Ниже представлены товары раздела {select_name_catalog[0]}</b>', reply_markup=ikb.give_product_in_catalog('give_', 's', req))
    else:
        await call.message.edit_text(f'<b>На данный момент нет товаров в разделе {select_name_catalog[0]}</b>', reply_markup=ikb.back_list_product('s', '0')) 


@dp.callback_query_handler(Text(startswith='give_product_'))
async def call_give_info_product(call: CallbackQuery):
    msg = call.data.split('_')

    with DB() as db:
        req = db.give_info_product(msg[2])
        isProduct = db.check_basket_product(call.message.chat.id, req[0][0])

    if req[0][5] != 0:
        await call.message.edit_text(f'<b>ID Товара</b> <code>#{req[0][0]}</code>\n'
                                    f'<b>Название товара:</b> {req[0][2]}\n'
                                    f'<b>Всего в базе:</b> {req[0][5]}\n'
                                    f'<b>Цена:</b> {float(req[0][4])}\n\n'
                                    f'<b>Описание:</b> \n{req[0][3]}\n', reply_markup=ikb.back_list_product(req[0][1], req[0][0], isProduct))
    else:
        await call.message.edit_text('<b>Тут пусто</b>', reply_markup=ikb.back_list_product(req[0][1], '0', isProduct))

@dp.callback_query_handler(Text(startswith='isProduct_'))
async def call_give_info_product(call: CallbackQuery):
    msg = call.data.split('_')
    print(msg)
    with DB() as db:
        req = db.give_info_product(msg[1])
        count_product = db.give_basket_product(call.message.chat.id, msg[1])

    if req[0][5] != 0:
        await call.message.edit_text(f'<b>ID Товара</b> <code>#{req[0][0]}</code>\n'
                                    f'<b>Название товара:</b> {req[0][2]}\n'
                                    f'<b>Кол-во товара:</b> {count_product[0][3]}\n'
                                    f'<b>Цена:</b> {float(req[0][4]) * float(count_product[0][3])} (x{count_product[0][3]})\n\n'
                                    f'<b>Описание:</b> {req[0][3]}\n', reply_markup=ikb.basket_product_menu(call.message.chat.id, msg[1], req[0][2], count_product[0][3], req[0][5]))