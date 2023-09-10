from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext

from keyboards import inline_keyboards as ikb
from keyboards import admin_keyboards as aikb
from states.state import AddProducts, AdvancedAddProducts
from data.db import DB
from loader import dp, bot
from handlers import commands as com


@dp.callback_query_handler(Text(startswith='add_products_'))
async def call_add_products(call: types.CallbackQuery):
    await call.message.edit_text('Выберите метод добавления продукта', reply_markup=ikb.select_add_product())


@dp.callback_query_handler(Text(startswith='select_add_product_'))
async def call_select_add_product(call: types.CallbackQuery, state: FSMContext):
    call_msg = call.data.split('_')
    with DB() as db:
        req = db.give_all_catalogs()

    if [] != req:
        if call_msg[3] == 'usual':
            await state.set_state(AddProducts.id_catalog)
        
        if call_msg[3] == 'advanced':
            await state.set_state(AdvancedAddProducts.id_catalog)
            
        await call.message.edit_text('Выберите каталог в котором хотите добавить товар', reply_markup=ikb.multi_control_category(req, db, 'add', 'product'))

    else:
        await call.message.edit_text('Для добавления товара в каталог вам необходимо сначала создать каталог', reply_markup=ikb.multi_control_category(req, db, 'add', 'product'))

# //////////////////////////////[Usual]/////////////////////////

@dp.callback_query_handler(Text(startswith='add_product_'), state=AddProducts.id_catalog)
async def call_add_product(call: types.CallbackQuery, state: FSMContext):
    call_msg = call.data.split('_')

    async with state.proxy() as data:
        data['id_catalog'] = call_msg[2]

    await state.set_state(AddProducts.product)
    await call.message.edit_text(f'Добавление товара в каталог <b>{call_msg[2]}</b>\n'
                                'Пришлите через теги <b>#tor#</b>: Имя товара#tor#Краткое описание#tor#Стоимость товара#tor#Количество товара#tor#Ссылку на товар\n\n'
                                '<b>Пример:</b> <code>Бравлстарс#tor#Сливаю по дешевке🔥жирный аккаунт много дорогих скинов💯 несколько купленных БП#tor#696#tor#2#tor#https://360.yandex.ru/disk/</code>', reply_markup=ikb.cance_add_new_product())


@dp.message_handler(state=AddProducts.product)
async def call_add_end(message: types.Message, state: FSMContext):
    _msg = message.text.split('#tor#')

    if len(_msg) == 5:
        if int(_msg[3]) > 1000000:
            await message.reply('Слишком больщое количество товара\n'
                                'Максимум 1000000\n'
                                '<b>Попробуйте снова:</b>')
            return

        try:
            int(_msg[2])
            int(_msg[3])
        except ValueError:
            await message.reply('Цена или количество товара должны быть числовыми\n\n<b>Попробуйте снова:</b>', reply_markup=ikb.cance_add_new_product())
            return
        
        if len(_msg[1]) > 151:
            await message.reply('Максимальное количество символов 150 в ОПИСАНИИ\n\n<b>Попробуйте снова:</b>', reply_markup=ikb.cance_add_new_product())

        elif not 'https://' in _msg[4]:
            await message.reply('Не видно ссылки на товар "https://"')

        elif len(_msg[0]) > 32:
            await message.reply('Максимальное количество символов 32 в Названии Товара\n\n<b>Попробуйте снова:</b>', reply_markup=ikb.cance_add_new_product())

        else:
            async with state.proxy() as data:
                with DB() as db:
                    db.add_product_in_catalogs(data['id_catalog'], _msg[0], _msg[1], float(_msg[2]), float(_msg[3]), _msg[4])
                    
            await com.delete_all_message_chat(message)
            await state.finish()
            await message.answer('Товар успешно добавлен в каталог и уже доступен пользователям!', reply_markup=aikb.main_admin_panel())

    else:
        await message.reply('Что то не так, перепроверьте теги #tor#, попробуйте как в примере\n\n<b>Имя товара#tor#Краткое описание#tor#Стоимость товара#tor#Количество товара#tor#Ссылку на товар\n\nПопробуйте снова:</b>', reply_markup=ikb.cance_add_new_product())

# //////////////////////////////[Advanced]/////////////////////////

@dp.callback_query_handler(Text(startswith='add_product_'), state=AdvancedAddProducts.id_catalog)
async def call_add_product_advanced(call: types.CallbackQuery, state: FSMContext):
    call_msg = call.data.split('_')
    
    async with state.proxy() as data:
        data['id_catalog'] = call_msg[2]

    await state.set_state(AdvancedAddProducts.name_product)

    await call.message.edit_text('<b>Пришлите название товара не более 64 символов</b>', reply_markup=ikb.select_add_or_cancel_product())


@dp.message_handler(state=AdvancedAddProducts.name_product)
async def call_add_name_product(message: types.Message, state: FSMContext):

    if len(message.text) > 64:
        await message.answer(f'Максимум 64 символов в названии товара, в вашем {len(message.text)} символов:')
        return
    
    async with state.proxy() as data:
        data['name_product'] = message.text

    await state.set_state(AdvancedAddProducts.description_product)
    await message.answer('<b>Пришлите краткое описание товара не более 600 символов</b>', reply_markup=ikb.select_add_or_cancel_product())
    await com.delete_all_message_chat(message)

@dp.message_handler(state=AdvancedAddProducts.description_product)
async def call_add_name_product(message: types.Message, state: FSMContext):

    if len(message.text) > 600:
        await message.answer(f'Максимум 600 символов в описании товара, в вашем {len(message.text)} символов:')
        return
    
    async with state.proxy() as data:
        data['description_product'] = message.text

    await state.set_state(AdvancedAddProducts.price_product)
    await message.answer('<b>Пришлите стоимость товара</b>', reply_markup=ikb.select_add_or_cancel_product())
    await com.delete_all_message_chat(message)

@dp.message_handler(state=AdvancedAddProducts.price_product)
async def call_add_name_product(message: types.Message, state: FSMContext):

    try:
        price_int = int(message.text)

        if price_int >= 1_000_000:
            await message.answer('<b>Слишком дорогой товар, максимум 1 000 000 RUB</b>')
            return
        
        async with state.proxy() as data:
            data['price_product'] = price_int

        await state.set_state(AdvancedAddProducts.count_product)

        await message.answer('<b>Пришлите количество товара</b>', reply_markup=ikb.select_add_or_cancel_product())

    except ValueError:
        await message.answer('<b>Введите число!</b>')
        return
    
    await com.delete_all_message_chat(message)

@dp.message_handler(state=AdvancedAddProducts.count_product)
async def call_add_name_product(message: types.Message, state: FSMContext):

    try:
        count_int = int(message.text)

        if count_int > 10000:
            await message.answer('<b>Слишком огромное количество товара, максимум 10 000</b>')
            return
        
        async with state.proxy() as data:
            data['count_product'] = count_int

        await state.set_state(AdvancedAddProducts.link_product)
        await message.answer('<b>Пришлите ссылку на товар который выдадут после его приобретения</b>', reply_markup=ikb.select_add_or_cancel_product())

    except ValueError:
        await message.answer('<b>Введите число!</b>')
        return

@dp.message_handler(state=AdvancedAddProducts.link_product)
async def call_add_name_product(message: types.Message, state: FSMContext):

    if len(message.text) >= 600:
        await message.answer('Слишком длинная ссылка')
        return
    
    if not 'https://' in message.text:
        await message.reply('Не видно ссылки на товар "https://"')
        return
    
    async with state.proxy() as data:
        _name_product = data['name_product']
        _description_product = data['description_product']
        _price_product = data['price_product']
        _count_product = data['count_product']
        data['link_product'] = message.text

    await state.set_state(AdvancedAddProducts.success)
    await com.delete_all_message_chat(message)
    await message.answer(f'<b>Название товара:</b> <code>{_name_product}</code>\n'
                         f'<b>Описание товара:</b> <code>{_description_product}</code>\n'
                         f'<b>Стоимость товара:</b> <code>{_price_product}</code> <b>RUB</b>\n'
                         f'<b>Количество товара:</b> <code>{_count_product}</code>\n'
                         f'<b>Ссылка на товар:</b> <code>{message.text}</code>\n')
    
    await message.answer('Проверьте добавляемый товар в каталог, если всё в поярдке нажмите "<b>Добавить</b>" или "<b>Отмена</b>" если передумали', reply_markup=ikb.select_add_or_cancel_product(True))

@dp.callback_query_handler(Text(startswith='add_product_advanced'), state=AdvancedAddProducts)
async def call_add_product_advanced(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        _id_catalog = data['id_catalog']
        _name_product = data['name_product']
        _description_product = data['description_product']
        _price_product = data['price_product']
        _count_product = data['count_product']
        _link_product = data['link_product']

        with DB() as db:
            db.add_product_in_catalogs(_id_catalog, _name_product, _description_product, float(_price_product), float(_count_product), _link_product)

    await state.finish()
    await call.message.edit_text('Товар успешно добавлен в каталог и уже доступен пользователям!', reply_markup=aikb.main_admin_panel())
    await com.delete_all_message_chat(call.message)