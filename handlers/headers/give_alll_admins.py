import aiogram
from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.storage import FSMContext

import asyncio

from states.state import PushAdminMessage, EditAdminBalance, EditAdminProcent
from data.db import DB
from libs.config import id_admin
from keyboards import inline_keyboards as ikb
from loader import dp, bot
from handlers import commands as com

# EN Here shows the Admins section, the list of admins and management
# RU Здесь показан раздел "Администраторы", список администраторов и руководства

@dp.callback_query_handler(text='management_admins_admin_')
async def call_management_admins_admin(call: types.CallbackQuery):
    list_admins = id_admin()

    if list_admins[0] == call.message.chat.id:
        with DB() as db:
            get_list_admins =  db.give_all_admin_list()

        msg_is_list_admins = '📋 <b>Список Админов Магазин Бота</b>'
        if [] == get_list_admins:
            msg_is_list_admins += '\n-<i>Список Админов пуст</i>'
            
        await call.message.edit_text(msg_is_list_admins, reply_markup=ikb.give_list_admins(get_list_admins))

    else:
        _id = await call.message.answer('📛 <b>У вас нет уполномочий урпавлять другими Админами</b>')
        await asyncio.sleep(2)
        try:
            await bot.delete_message(call.message.chat.id, message_id=_id.message_id)
        except aiogram.utils.exceptions.MessageToDeleteNotFound:
            pass

@dp.callback_query_handler(Text(startswith='give_admin_id_'))
async def call_give_admin_id(call: types.CallbackQuery):
    call_msg = call.data.split('_')

    with DB() as db:
        get_info = db.give_info_user('name, lastname, balance_rub, procent, all_money_deposit', call_msg[3])
        get_karma_admin = db.give_karma_admin(int(call_msg[3]))

    await call.message.edit_text(f'🆔 <b>Админ:</b> <code>{call_msg[3]}</code>\n'
                                 f'🪪 <b>FullName: {get_info[0]} {get_info[1]}</b>\n'
                                 f'💳 <b>Баланс: {get_info[2]} RUB</b>\n'
                                 f'💸 <b>Всего Депозит: {get_info[4]}</b>\n'
                                 f'🔮 <b>Карма: {get_karma_admin[0]}</b>\n'
                                 f'⚖️ <b>Процент от пополнений: {get_info[3]}</b>', reply_markup=ikb.edit_admins(call_msg[3]))


@dp.callback_query_handler(Text(startswith='del_admin_id_'))
async def call_del_admin_id(call: types.CallbackQuery):
    call_msg = call.data.split('_')
    with DB() as db:
        db.delete_admins(call_msg[3])

    await call.message.edit_text(f'💢 <b>Админ:</b> <code>{call_msg[3]}</code> был удалён из списка Админов', reply_markup=ikb.back_in_edit_admins())


@dp.callback_query_handler(Text(startswith='push_msg_admin_id_'))
async def call_push_msg_admin_id(call: types.CallbackQuery, state: FSMContext):
    call_msg = call.data.split('_')
    await state.set_state(PushAdminMessage.admin_push_message)

    async with state.proxy() as data:
        data['id_admin'] = call_msg[4]

    await call.message.edit_text(f'📝 <b>Пришлите сообщение для Админа {call_msg[4]} максимум 800 символов:</b>',
                                 reply_markup=ikb.cancel_in_edit_admins('PushAdminMessage'))


@dp.message_handler(state=PushAdminMessage.admin_push_message)
async def admin_push_msg(message: types.Message, state: FSMContext):

    if len(message.text) > 800:
        await message.answer(f'⛔️ <b>Максимум 800 символов в сообщении:</b>\nВаше сообщение содержит {len(message.text)} символов',
                             reply_markup=ikb.cancel_in_edit_admins('PushAdminMessage'))
        return
    
    async with state.proxy() as data:
        _id_admin = data['id_admin']

    try:
        await bot.send_message(_id_admin, message.text)
        await message.answer(f'✅ <b>Сообщение успешно было отправлено Админу {_id_admin}</b>')
    except:
        await message.answer(f'⚠️ <b>Ощибка\nНе получилось отправить сообщение Админу {_id_admin}\nВозможно заблокировал бота</b>')
    
    await state.finish()


@dp.callback_query_handler(Text(startswith='edit_balance_admin_id_'))
async def call_push_msg_admin_id(call: types.CallbackQuery, state: FSMContext):
    call_msg = call.data.split('_')

    async with state.proxy() as data:
        data['id_admin'] = call_msg[4]
    
    await state.set_state(EditAdminBalance.admin_balance_rub)
    await call.message.edit_text('✏️ Отправьте баланс который хотите установить\n\n<b>Если хотите изменить от текущего баланса отправьте число с плюсом +100 или минусом -100</b>',
                                 reply_markup=ikb.cancel_in_edit_admins('EditAdminBalance'))


@dp.message_handler(state=EditAdminBalance.admin_balance_rub)
async def edit_admin_balance_rub(message: types.Message, state: FSMContext):
    
    try:
        _int_summ_balance_admin = int(message.text)
    except ValueError:
        await message.answer('⛔️ <b>Введите число!</b>', reply_markup=ikb.cancel_in_edit_admins('EditAdminBalance'))
        return
    
    async with state.proxy() as data:
        _id_admin = data['id_admin']


    with DB() as db:
        if '+' in message.text:
            db.give_top_up_balance_rub(_id_admin, _int_summ_balance_admin)
            try:
                await bot.send_message(_id_admin, f'ℹ️ Ваш баланс был изменён на <b>{message.text} RUB</b>')
            except:
                pass            
            await message.answer(f'✅ Баланс Админа <code>{_id_admin}</code> изменён на <b>{message.text} RUB</b>',
                                 reply_markup=ikb.back_in_edit_admins())
            await state.finish()
            return
        
        if '-' in message.text:
            db.give_top_up_balance_rub(_id_admin, _int_summ_balance_admin)
            try:
                await bot.send_message(_id_admin, f'ℹ️ Ваш баланс был изменён на <b>{message.text} RUB</b>')
            except:
                pass
            await message.answer(f'✅ Баланс Админа <code>{_id_admin}</code> изменён на <b>{message.text} RUB</b>',
                                 reply_markup=ikb.back_in_edit_admins())
            await state.finish()
            return

        
        db.update_multi_balance_user(_int_summ_balance_admin, _id_admin)
        try:
            await bot.send_message(_id_admin, f'💬 Ваш баланс был установлен <b>{message.text} RUB</b>')
        except:
            await message.answer('⚠️ <i>Не получилось оповестить Админа об изменении его баланса</i>')

        await message.answer(f'✅ Баланс Админа <code>{_id_admin}</code> установлен <b>{message.text} RUB</b>',
                             reply_markup=ikb.back_in_edit_admins())
        await state.finish()


@dp.callback_query_handler(Text(startswith='edit_procent_admin_id_'))
async def call_push_msg_admin_id(call: types.CallbackQuery, state: FSMContext):
    call_msg = call.data.split('_')
    
    await state.set_state(EditAdminProcent.admin_procent)

    async with state.proxy() as data:
        data['id_admin'] = call_msg[4]

    await call.message.edit_text('✏️ Отправьте процент при пополнении баланса от 0 до 100 без "%"\n\n'
                                 'ℹ️ <b>Это процент который начислится Админу на его баланс от его суммы пополнения</b>',
                                 reply_markup=ikb.cancel_in_edit_admins('EditAdminProcent'))


@dp.message_handler(state=EditAdminProcent.admin_procent)
async def call_add_procent_user(message: types.Message, state: FSMContext):
    await com.delete_all_message_chat(message)
    try:
        _procent_user = int(message.text)
    except ValueError:
        await message.answer('📝 <b>Отправьте процент от 0 до 100:</b>',
                             reply_markup=ikb.cancel_in_edit_admins('EditAdminProcent'))
        return
    
    if _procent_user > 100:
        await message.answer('⛔️ <b>Максимальный процент 100</b>',
                             reply_markup=ikb.cancel_in_edit_admins('EditAdminProcent'))
        return
    
    if _procent_user < 0:
        await message.answer('⛔️ <b>Минимальный процент 0</b>',
                             reply_markup=ikb.cancel_in_edit_admins('EditAdminProcent'))
        return
    
    async with state.proxy() as data:
        _id_admin = data['id_admin']

    with DB() as db:
        db.update_procent_users(_procent_user, _id_admin)

    await message.answer(f'✅ <b>Процент Админа {_id_admin} установлен {_procent_user}%</b>',
                         reply_markup=ikb.back_in_edit_admins())
    await state.finish()