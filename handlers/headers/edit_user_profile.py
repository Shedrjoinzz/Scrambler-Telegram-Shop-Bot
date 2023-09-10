from aiogram import types
import aiogram
from aiogram.dispatcher.storage import FSMContext
from aiogram.dispatcher.filters import Text

import asyncio

from data.db import DB
from loader import dp, bot
from states.state import EditUserInfo
from keyboards import inline_keyboards as ikb
from handlers import commands as com

@dp.callback_query_handler(text='info_user')
async def call_info_user(call: types.CallbackQuery, state: FSMContext):
    await state.set_state(EditUserInfo.id_user)
    await call.message.edit_text('<b>Отправьте ID пользователя</b>', reply_markup=ikb.cancel_method('cancel_info_user'))

@dp.message_handler(state=EditUserInfo.id_user)
async def edit_user_info(message: types.Message, state: FSMContext):
    try:
        _id_user = int(message.text)
    except ValueError:
        await message.answer('<b>Отправьте ID!</b>', reply_markup=ikb.cancel_method('cancel_info_user'))
        return

    async with state.proxy() as data:
        data['id_user'] = _id_user

    with DB() as db:
        get_info_user = db.give_info_user('*', _id_user)
        get_ban_list_user = db.give_is_ban_users(_id_user)
    
    if get_info_user is None:
        await message.answer('<b>Такого пользователя нет в боте</b>', reply_markup=ikb.cancel_method('cancel_info_user'))
        return
    

    await message.answer(f'<b>Профиль пользователя</b>\n'
                        f'<b>UserCode:</b> {get_info_user[0]}\n'
                        f'<b>ID:</b> <code>{get_info_user[1]}</code>\n'
                        f'<b>Баланс:</b> <code>{get_info_user[2]}</code> <b>RUB</b>\n'
                        f'<b>Процент при пополнении:</b> {get_info_user[3]}% <b>(один раз)</b>\n'
                        f'<b>Статус Бан:</b> {get_ban_list_user}'.replace("True", "Заблокирован 🔴").replace("False", "Разблокирован 🟢"), reply_markup=ikb.select_one_user_manager(get_info_user[1]))

    await com.delete_all_message_chat(message)


@dp.callback_query_handler(text='edit_balance_user', state=EditUserInfo.id_user)
async def call_edit_balance_user(call: types.CallbackQuery, state: FSMContext):
    await state.set_state(EditUserInfo.summ_balance)
    await call.message.edit_text('Отправьте баланс который хотите установить\n\n<b>Если хотите изменить от текущего баланса отправьте число с плюсом +100 или минусом -100</b>', reply_markup=ikb.cancel_method('cancel_info_user'))


@dp.message_handler(state=EditUserInfo.summ_balance)
async def message_add_new_balance_user(message: types.Message, state: FSMContext):
    try:
        _int_summ_balance = int(message.text)
    except ValueError:
        await message.answer("<b>Введите число!</b>", reply_markup=ikb.cancel_method('cancel_info_user'))
        return
    
    async with state.proxy() as data:
        _id_user = data['id_user']
        
    with DB() as db:
        if '+' in message.text:
            db.give_top_up_balance_rub(_id_user, _int_summ_balance)
            try:
                await bot.send_message(_id_user, f'Ваш баланс был изменён на <b>{message.text} RUB</b>')
            except:
                pass            
            await message.answer(f'Баланс пользователя <code>{_id_user}</code> изменён на <b>{message.text} RUB</b>', reply_markup=ikb.user_edit_button())
            await state.finish()
            return
        
        if '-' in message.text:
            db.give_top_up_balance_rub(_id_user, _int_summ_balance)
            try:
                await bot.send_message(_id_user, f'Ваш баланс был изменён на <b>{message.text} RUB</b>')
            except:
                pass
            await message.answer(f'Баланс пользователя <code>{_id_user}</code> изменён на <b>{message.text} RUB</b>', reply_markup=ikb.user_edit_button())
            await state.finish()
            return

        
        db.update_multi_balance_user(_int_summ_balance, _id_user)
        try:
            await bot.send_message(_id_user, f'Ваш баланс был установлен <b>{message.text} RUB</b>')
        except:
            pass
        await message.answer(f'Баланс пользователя <code>{_id_user}</code> установлен <b>{message.text} RUB</b>', reply_markup=ikb.user_edit_button())
        await state.finish()


@dp.callback_query_handler(Text(startswith='edit_status_user_'), state=EditUserInfo.id_user)
async def call_ban_user_edit(call: types.CallbackQuery, state: FSMContext):
        call_msg = call.data.split('_')
        
        async with state.proxy() as data:
            _id_user = data['id_user']

            with DB() as db:
                get_info_user = db.give_info_user('*', _id_user)
                get_ban_list_user = db.give_is_ban_users(_id_user)


            if call_msg[3] == 'ban':
                if get_ban_list_user:
                    await call.message.edit_text('<b>Пользователь и так Заблокирован 🟣</b>')

                if get_ban_list_user == False:
                    await state.set_state(EditUserInfo.info_ban_user)
                    await call.message.edit_text(f'<b>Пришлите причину Бана пользователя ID</b> <code>{_id_user}</code>'
                                                 '<b>максимум 800 символов или пришлите "-" что-бы оставить описание причины Бана Пустым</b>',
                                                 reply_markup=ikb.cancel_method('cancel_info_user'))
                    return
                
            if call_msg[3] == 'unban':
                if get_ban_list_user == False:
                    await call.message.edit_text('<b>Пользователь и так Разблокирован 🟣</b>')
                
                if get_ban_list_user:
                    db.update_ban_list('unban', _id_user, '-')
                    await call.message.edit_text(f'<b>Пользователь Разблокирован 🟢</b>')
            
            await asyncio.sleep(1)
            get_ban_list_user = db.give_is_ban_users(_id_user)

            try:
                await call.message.edit_text(f'<b>Профиль пользователя</b>\n'
                                            f'<b>UserCode:</b> {get_info_user[0]}\n'
                                            f'<b>ID:</b> <code>{get_info_user[1]}</code>\n'
                                            f'<b>Баланс:</b> <code>{get_info_user[2]}</code> <b>RUB</b>\n'
                                            f'<b>Процент при пополнении:</b> {get_info_user[3]}% <b>(один раз)</b>\n'
                                            f'<b>Статус Бан:</b> {get_ban_list_user}'.replace("True", "Заблокирован 🔴").replace("False", "Разблокирован 🟢"),
                                            reply_markup=ikb.select_one_user_manager(get_info_user[1]))
                
            except aiogram.exceptions.MessageToEditNotFound:
                print('aiogram: Message to edit not found\n\nСообщение для редактирования не найдено')
            except aiogram.exceptions.MessageNotModified:
                print('aiogram: Message is not modified: specified new message content and reply markup are exactly the same as a current content and reply markup of the message\n\n'
                      'Сообщение не изменено: указанное содержимое нового сообщения и ответная разметка точно такие же, как текущее содержимое и ответная разметка сообщения')


@dp.message_handler(state=EditUserInfo.info_ban_user)
async def info_user_ban_handler(message: types.Message, state: FSMContext):

    if len(message.text) > 800:
        await message.answer('<b>Максимум 800 символов в описании причины Бана пользователя или пришлите "-" что-бы оставить описание причины Бана Пустым:</b>',
                             reply_markup=ikb.cancel_method('cancel_info_user'))
        return

    msg_user_ban = '<b>Вы были заблокированы Администрацией!</b>'

    async with state.proxy() as data:
        _id_user = data['id_user']
    
    with DB() as db:
        db.update_ban_list('ban', _id_user, message.text)
        if message.text != '-':    
            msg_user_ban += f'\n\n<b>Причина Бана:</b> <i>{message.text}</i>'
            
    try:
        await bot.send_message(_id_user, msg_user_ban)
    except:
        pass
    await state.finish()
    await message.answer(f'<b>Пользователь Заблокирован 🔴!</b>\n\nПричина Бана: <i>{message.text}</i>', reply_markup=ikb.user_edit_button())


@dp.callback_query_handler(Text(startswith='edit_procent_user'), state=EditUserInfo.id_user)
async def call_edit_procent_user(call: types.CallbackQuery, state: FSMContext):
    await state.set_state(EditUserInfo.procent)
    await call.message.edit_text('Отправьте процент при пополнении баланса от 0 до 100 без "%"\n\n'
                                 '<b>Это процент который начислится пользователю на его баланс от его суммы пополнения</b>',
                                 reply_markup=ikb.cancel_method('cancel_info_user'))


@dp.message_handler(state=EditUserInfo.procent)
async def call_add_procent_user(message: types.Message, state: FSMContext):
    await com.delete_all_message_chat(message)
    try:
        _procent_user = int(message.text)
    except ValueError:
        await message.answer('<b>Отправьте процент от 0 до 100:</b>', reply_markup=ikb.cancel_method('cancel_info_user'))
        return
    
    if _procent_user > 100:
        await message.answer('<b>Максимальный процент 100</b>', reply_markup=ikb.cancel_method('cancel_info_user'))
        return
    
    if _procent_user < 0:
        await message.answer('<b>Минимальный процент 0</b>', reply_markup=ikb.cancel_method('cancel_info_user'))
        return
    
    async with state.proxy() as data:
        _id_user = data['id_user']

    with DB() as db:
        db.update_procent_users(_procent_user, _id_user)

    await message.answer(f'<b>Процент пользователя {_id_user} установлен {_procent_user}</b>', reply_markup=ikb.user_edit_button())
    await state.finish()


@dp.callback_query_handler(Text(startswith='push_msg_one_user'), state=EditUserInfo.id_user)
async def call_push_msg_one_user(call: types.CallbackQuery, state: FSMContext):
    await state.set_state(EditUserInfo.push_msg_user)
    await com.delete_all_message_chat(call.message)
    async with state.proxy() as data:
        _id_user = data['id_user']

    await call.message.edit_text(f'Отправьте сообщение для пользователя <b>{_id_user}</b> максимум 800 символов\n\n'
                                 '<b>[?]</b> Это односторонняя коммуникация, пользователь будет просто извещён вашим сообщением\n'
                                 '<b>[?]</b> Для двухсторонней коммуникации перейдите в раздел <b>Админка->Сообщения</b>',
                                 reply_markup=ikb.cancel_method('cancel_info_user'))
    
@dp.message_handler(state=EditUserInfo.push_msg_user)
async def push_message_user(message: types.Message, state: FSMContext):
    await com.delete_all_message_chat(message)
    if len(message.text) > 800:
        await message.answer('<b>Максимум 800 символов в сообщении:</b>\n'
                             f'<i>В вашем сообщении {len(message.text)} символов</i>',
                                 reply_markup=ikb.cancel_method('cancel_info_user'))
        return
    
    async with state.proxy() as data:
        _id_user = data['id_user']

    try:
        await bot.send_message(_id_user, f'<b>АДМИН:</b> <i>{message.text}</i>')
    except:
        await message.answer('<b>Не получилось известить пользователя</b>')
        await state.finish()
        return

    await state.finish()
    await message.answer('<b>Пользователь успешно был извещён!</b>',
                         reply_markup=ikb.user_edit_button())



