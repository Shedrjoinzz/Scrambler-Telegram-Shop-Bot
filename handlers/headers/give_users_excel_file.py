from aiogram import types
import aiogram

import pandas as pd

from keyboards import inline_keyboards as ikb
from data.db import DB
from loader import dp, bot


@dp.callback_query_handler(text='get_all_info_excel')
async def call_get_all_info_excel(call: types.CallbackQuery):
    await call.message.edit_text('<b>Выберите что хотите экспортировать</b>\nЭто может занять некоторое время', reply_markup=ikb.export_data_shop())
    

@dp.callback_query_handler(text='export_users')
async def call_export_data_table(call: types.CallbackQuery):
    with DB() as db:
        get_table_info = db.give_all_from_table_method('users')

        if [] == get_table_info:
            await call.message.edit_text('Данные отсутствуют в таблице (users)', reply_markup=ikb.back_excel_data())
            return
        
        _excel = {'UserCode': [],
                    'User ID': [],
                    'Balance RUB': [],
                    'Procent': [],
                    'First Name': [],
                    'Last Name': [],
                    'Username': [],
                    'Lang Code': []}

        for i in get_table_info:
            _excel['UserCode'].append(i[0])
            _excel['User ID'].append(i[1])
            _excel['Balance RUB'].append(i[2])
            _excel['Procent'].append(i[3])
            _excel['First Name'].append(i[4])
            _excel['Last Name'].append(i[5])
            _excel['Username'].append(i[6])
            _excel['Lang Code'].append(i[7])

        
        await output_excel_file_tables(call.message, 'handlers/headers/excel_output/', 'users', _excel)

@dp.callback_query_handler(text='export_admins')
async def call_export_data_table(call: types.CallbackQuery):
    with DB() as db:
        get_table_info = db.give_all_from_table_method('admins')
        
        if [] == get_table_info:
            await call.message.edit_text('Данные отсутствуют в таблице (admins)', reply_markup=ikb.back_excel_data())
            return

        _excel = {'UserCode': [],
                    'Admins ID': [],
                    'Full Name': []}

        for i in get_table_info:
            _excel['UserCode'].append(i[0])
            _excel['Admins ID'].append(i[1])
            _excel['Full Name'].append(i[2])

            
        await output_excel_file_tables(call.message, 'handlers/headers/excel_output/', 'admins', _excel)


@dp.callback_query_handler(text='export_ban_list')
async def call_export_data_table(call: types.CallbackQuery):
    with DB() as db:
        get_table_info = db.give_all_from_table_method('ban_list')
        
        if [] == get_table_info:
            await call.message.edit_text('Данные отсутствуют в таблице (ban_list)', reply_markup=ikb.back_excel_data())
            return

        _excel = {'UserCode': [],
                    'User ID': [],
                    'Info What Banned': []}

        for i in get_table_info:
            _excel['UserCode'].append(i[0])
            _excel['User ID'].append(i[1])
            _excel['Info What Banned'].append(i[2])

            
        await output_excel_file_tables(call.message, 'handlers/headers/excel_output/', 'ban_list', _excel)


@dp.callback_query_handler(text='export_catalogs')
async def call_export_data_table(call: types.CallbackQuery):
    with DB() as db:
        get_table_info = db.give_all_from_table_method('catalogs')
        
        if [] == get_table_info:
            await call.message.edit_text('Данные отсутствуют в таблице (catalogs)', reply_markup=ikb.back_excel_data())
            return

        _excel = {'Catalog ID': [],
                    'Catalog Name': []}

        for i in get_table_info:
            _excel['Catalog ID'].append(i[0])
            _excel['Catalog Name'].append(i[1])
            
        await output_excel_file_tables(call.message, 'handlers/headers/excel_output/', 'catalogs', _excel)


@dp.callback_query_handler(text='export_products')
async def call_export_data_table(call: types.CallbackQuery):
    with DB() as db:
        get_table_info = db.give_all_from_table_method('products')
        
        if [] == get_table_info:
            await call.message.edit_text('Данные отсутствуют в таблице (products)', reply_markup=ikb.back_excel_data())
            return

        _excel = {'Product ID': [],
                    'Catalog ID': [],
                    'Product Name': [],
                    'Product Description': [],
                    'Product Price': [],
                    'Product Count': [],
                    'Product Link': []}

        for i in get_table_info:
            _excel['Product ID'].append(i[0])
            _excel['Catalog ID'].append(i[1])
            _excel['Product Name'].append(i[2])
            _excel['Product Description'].append(i[3])
            _excel['Product Price'].append(i[4])
            _excel['Product Count'].append(i[5])
            _excel['Product Link'].append(i[6])

            
        await output_excel_file_tables(call.message, 'handlers/headers/excel_output/', 'products', _excel)

@dp.callback_query_handler(text='export_basket')
async def call_export_data_table(call: types.CallbackQuery):
    with DB() as db:
        get_table_info = db.give_all_from_table_method('basket')
        
        if [] == get_table_info:
            await call.message.edit_text('Данные отсутствуют в таблице (basket)', reply_markup=ikb.back_excel_data())
            return

        _excel = {'User ID': [],
                    'Product ID': [],
                    'Catalog ID': [],
                    'Product Count Buy': []}

        for i in get_table_info:
            _excel['User ID'].append(i[0])
            _excel['Product ID'].append(i[1])
            _excel['Catalog ID'].append(i[2])
            _excel['Product Count Buy'].append(i[3])

            
        await output_excel_file_tables(call.message, 'handlers/headers/excel_output/', 'basket', _excel)


@dp.callback_query_handler(text='export_manager_bot')
async def call_export_data_table(call: types.CallbackQuery):
    with DB() as db:
        get_table_info = db.give_all_from_table_method('manager_bot')
        
        if [] == get_table_info:
            await call.message.edit_text('Данные отсутствуют в таблице (manager_bot)', reply_markup=ikb.back_excel_data())
            return

        _excel = {'Message Is Buy Product': [],
                    'Message Is Start': [],
                    'Message Is New User': [],
                    'Status Bot': [],
                    'Max Summ Top Up': [],
                    'Min Summ Top Up': [],
                    'Message Is FAQ': [],
                    'Message Service Bot': [],
                    'Deduction': []}

        for i in get_table_info:
            _excel['Message Is Buy Product'].append(i[0])
            _excel['Message Is Start'].append(i[1])
            _excel['Message Is New User'].append(i[2])
            _excel['Status Bot'].append(i[3])
            _excel['Max Summ Top Up'].append(i[4])
            _excel['Min Summ Top Up'].append(i[5])
            _excel['Message Is FAQ'].append(i[6])
            _excel['Message Service Bot'].append(i[7])
            _excel['Deduction'].append(i[8])

            
        await output_excel_file_tables(call.message, 'handlers/headers/excel_output/', 'manager_bot', _excel)


@dp.callback_query_handler(text='export_statistic_finance')
async def call_export_data_table(call: types.CallbackQuery):
    with DB() as db:
        get_table_info = db.give_all_from_table_method('statistic_finance')
        
        if [] == get_table_info:
            await call.message.edit_text('Данные отсутствуют в таблице (statistic_finance)', reply_markup=ikb.back_excel_data())
            return

        _excel = {'All Money Main Admin': []}

        for i in get_table_info:
            _excel['All Money Main Admin'].append(i[0])

        await output_excel_file_tables(call.message, 'handlers/headers/excel_output/', 'statistic_finance', _excel)


async def output_excel_file_tables(message: types.Message, path, name_table, _excel):
        _id_msg = await message.answer('Ожидайте...')
        df_excel = pd.DataFrame(_excel)

        df_excel.to_excel(f'{path}table_info_{name_table}.xlsx')
        with open(f'{path}table_info_{name_table}.xlsx', 'rb') as xlsx:
            try:
                await bot.delete_message(message.chat.id, message_id=_id_msg.message_id)
            except aiogram.utils.exceptions.MessageToDeleteNotFound:
                pass
            await message.reply_document(xlsx)