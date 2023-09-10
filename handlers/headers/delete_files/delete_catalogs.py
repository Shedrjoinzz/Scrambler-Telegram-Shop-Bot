from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.storage import FSMContext

from data.db import DB
from loader import dp
from keyboards import inline_keyboards as ikb

@dp.callback_query_handler(Text(startswith='delete_catalogs_'))
async def call_delete_basket_prducts(call: types.CallbackQuery):
    with DB() as db:
        req = db.give_all_catalogs()
    if req != []:
        await call.message.edit_text('Выберите каталог который хотите удалить', reply_markup=ikb.multi_control_category(req, db, 'delete', 'delete_catalog'))
    else:
        await call.message.edit_text('Каталоги отсутствуют, создайте каталог', reply_markup=ikb.multi_control_category(req, db, 'None', 'catalog'))
        

@dp.callback_query_handler(Text(startswith='delete_catalog_'))
async def call_method_delete_catalog_(call: types.CallbackQuery):
    call_msg = call.data.split('_')
    with DB() as db:
        gets = db.give_all_product_in_catalogs(call_msg[2])
        _name = db.give_name_catalogs(call_msg[2])
        # select_all_product_in_catalog = db.give_all_product_in_catalogs(call_msg[2])
        if [] != gets:
            await call.message.edit_text(f'<b>Вы действительно хотите удалить {_name[0]} каталог?</b>\n'
                                        f'В {_name[0]} каталоге {len(gets)} товар-ов\n\n'
                                        f'<b>[?]</b> <i>После удаления каталога {_name[0]} будет удалено всё содежимое!</i>\n'
                                        '<b>[?]</b> <i>Так-же будет удалено всё у пользователей которые добавляли товар с этого каталога!</i>\n\n'
                                        'Для подтверждения нажмите Удалить или Отмена, если передумали', reply_markup=ikb.success_delete_catalog(call_msg[2]))
        else:
            db.delete_from_catalogs(call_msg[2])
            req = db.give_all_catalogs()
            await call.message.edit_text(f'Каталог {_name[0]} успешно был удалён!', reply_markup=ikb.multi_control_category(req, db, 'delete', 'delete_catalog'))

@dp.callback_query_handler(Text(startswith='successfully_delete_catalog_'))
async def call_success_delete_catalog(call: types.CallbackQuery):
    call_msg = call.data.split('_')
    with DB() as db:
        _name = db.give_name_catalogs(call_msg[3])
        db.delete_from_catalogs(call_msg[3])
        req = db.give_all_catalogs()
    await call.message.edit_text(f'Каталог {_name[0]} успешно был удалён!', reply_markup=ikb.multi_control_category(req, db, 'delete', 'delete_catalog'))

@dp.callback_query_handler(Text(startswith='delete_all_catalog_'))
async def call_delete_all_product(call: types.CallbackQuery):
    with DB() as db:
        db.delete_all_catalogs_one_clicked()
        req = db.give_all_catalogs()
    await call.message.edit_text('<b>Все каталоги успешно удалены</b>\n\nКаталогов больще нет', reply_markup=ikb.multi_control_category(req, db, 'delete', 'delete_catalog'))