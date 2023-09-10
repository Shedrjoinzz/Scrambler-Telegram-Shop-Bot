from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.storage import FSMContext

from states.state import *
from keyboards import inline_keyboards as ikb
from keyboards import admin_keyboards as aikb
from . import user_panel as usikb
from . import commands as com
from loader import dp
from data.db import DB


# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\AddCountInBasket\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
@dp.callback_query_handler(text='AddCountInBasket_close')
async def call_add_end(call: types.CallbackQuery):
    await com.delete_all_message_chat(call.message)
    await call.message.edit_text(f'Отмена добавления товара в корзину', reply_markup=usikb.user_panel(call.message.chat.id))


@dp.callback_query_handler(text='add_count_product_cancel', state=CountAddBasketProduct)
async def call_cancel_state(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await com.delete_all_message_chat(call.message)
    await call.message.edit_text(f'Отмена добавления товара в корзину', reply_markup=usikb.user_panel(call.message.chat.id))
# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\


# /////////////////////////////////////////EditCountInBasket///////////////////////////////////////////////////////////
@dp.callback_query_handler(text='EditCountInBasket_cancel', state=CountBasketProduct)
async def call_cancel_state(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await com.delete_all_message_chat(call.message)
    await call.message.edit_text(f'Отмена изменения товара в корзине', reply_markup=usikb.user_panel(call.message.chat.id))


@dp.callback_query_handler(text='EditCountInBasket_close')
async def call_cancel_state(call: types.CallbackQuery):
    await com.delete_all_message_chat(call.message)
    await call.message.edit_text(f'Отмена изменения товара в корзине', reply_markup=usikb.user_panel(call.message.chat.id))
# ////////////////////////////////////////////////////////////////////////////////////////////////////


@dp.callback_query_handler(Text(startswith='cancel_add_new_product'), state=AddProducts)
async def call_cancel_add_new_product(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await com.delete_all_message_chat(call.message)
    await call.message.edit_text('Админ панель', reply_markup=aikb.main_admin_panel())


@dp.callback_query_handler(text='cancel_state_in_add_product_', state=AddProducts)
async def call_add_end(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await com.delete_all_message_chat(call.message)
    await call.message.edit_text(f'Отмена добавления товара в корзину', reply_markup=usikb.user_panel(call.message.chat.id))


@dp.callback_query_handler(Text(startswith='exit_from_messenger_'), state=[MessengerUser, MessengerAdmin])
async def call_MessengerUser_exit_from_messenger(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    with DB() as db:
        get_is_start = db.give_message_is_start_and_message_is_buy_and_status_bot_and_captcha()
    await com.delete_all_message_chat(call.message)
    if get_is_start[0] == '-':
        await call.message.edit_text('<b>Главное меню</b>', reply_markup=usikb.user_panel(call.message.chat.id))
        return
    await call.message.edit_text(f'{get_is_start[0]}'.replace("%first_name%", call.from_user.first_name).replace("%username%", call.from_user.username).replace("%user_id%", f"{call.from_user.id}"), reply_markup=usikb.user_panel(call.message.chat.id))


@dp.callback_query_handler(Text(startswith='cancel_spam_'), state=SpamUsers)
async def call_cancel_spam(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.edit_text('Рассылка отменена', reply_markup=aikb.main_admin_panel())
    await com.delete_all_message_chat(call.message)


@dp.callback_query_handler(Text(startswith='cancel_product_advanced'), state=[i for i in [AdvancedAddProducts, AddProducts]])
async def call_add_product_advanced(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.edit_text('Отмена добавления товара в каталог', reply_markup=aikb.main_admin_panel())
    await com.delete_all_message_chat(call.message)


@dp.callback_query_handler(Text(startswith='cancel_edit_one_product'), state=EditProductOne)
async def call_cancel_edit_one_product(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.edit_text('<b>Отмена изменения товара</b>', reply_markup=aikb.main_admin_panel())
    await com.delete_all_message_chat(call.message)


@dp.callback_query_handler(Text(startswith='cancel_support'), state=Support)
async def call_cancel_edit_one_product(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    with DB() as db:
        get_is_start = db.give_message_is_start_and_message_is_buy_and_status_bot_and_captcha()

    await com.delete_all_message_chat(call.message)
    
    if get_is_start[0] == '-':
        await call.message.edit_text('<b>Главное меню</b>', reply_markup=usikb.user_panel(call.message.chat.id))
        return
    
    await call.message.edit_text(f'{get_is_start[0]}'.replace("%first_name%", call.from_user.first_name).replace("%username%", call.from_user.username).replace("%user_id%", f"{call.from_user.id}"), reply_markup=usikb.user_panel(call.message.chat.id))


@dp.callback_query_handler(Text(startswith='cancel_top_up_balance_user'), state=TopUpBalance)
async def call_cancel_edit_one_product(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    with DB() as db:
        get_is_start = db.give_message_is_start_and_message_is_buy_and_status_bot_and_captcha()

    await com.delete_all_message_chat(call.message)

    if get_is_start[0] == '-':
        await call.message.edit_text('<b>Главное меню</b>', reply_markup=usikb.user_panel(call.message.chat.id))
        return
    
    await call.message.edit_text(f'{get_is_start[0]}'.replace("%first_name%", call.from_user.first_name).replace("%username%", call.from_user.username).replace("%user_id%", f"{call.from_user.id}"), reply_markup=usikb.user_panel(call.message.chat.id))


@dp.callback_query_handler(text='cancel_info_user', state=EditUserInfo)
async def call_cancel_info_user(call: types.CallbackQuery, state: FSMContext):

    await state.finish()
    
    await call.message.edit_text('<b>Выберите раздел</b>', reply_markup=ikb.select_users_manager())
    
    await com.delete_all_message_chat(call.message)

@dp.callback_query_handler(text='cancel_edit_procent_all_users', state=EditProcentAllUsers)
async def call_cancel_info_user(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.edit_text('<b>Выберите раздел</b>', reply_markup=ikb.select_users_manager())
    await com.delete_all_message_chat(call.message)

@dp.callback_query_handler(text='cancel_edit_admins_EditAdminBalance', state=EditAdminBalance)
async def call_cancel_info_user(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    with DB() as db:
        get_list_admins =  db.give_all_admin_list()

    await call.message.edit_text('<b>Список Админов Магазин Бота</b>', reply_markup=ikb.give_list_admins(get_list_admins))
    await com.delete_all_message_chat(call.message)

@dp.callback_query_handler(text='cancel_edit_admins_EditAdminProcent', state=EditAdminProcent)
async def call_cancel_info_user(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    with DB() as db:
        get_list_admins =  db.give_all_admin_list()

    await call.message.edit_text('<b>Список Админов Магазин Бота</b>', reply_markup=ikb.give_list_admins(get_list_admins))
    await com.delete_all_message_chat(call.message)

@dp.callback_query_handler(text='cancel_edit_admins_PushAdminMessage', state=PushAdminMessage)
async def call_cancel_info_user(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    with DB() as db:
        get_list_admins =  db.give_all_admin_list()

    await call.message.edit_text('<b>Список Админов Магазин Бота</b>', reply_markup=ikb.give_list_admins(get_list_admins))
    await com.delete_all_message_chat(call.message)


@dp.callback_query_handler(text='cancel_reply_message', state = [i for i in [ToAskAdmin, NotifyAdmin, ToAskUsers, SetInfoBanUsers]])
async def call_cancel_info_user(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.delete()
