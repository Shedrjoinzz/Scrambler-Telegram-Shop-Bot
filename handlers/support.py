import aiogram
from aiogram import types
from aiogram.dispatcher.storage import FSMContext
from aiogram.dispatcher.filters import Text

from data.db import DB
from loader import dp, bot
from states.state import Support, ToAskAdmin, NotifyAdmin, ToAskUsers, SetInfoBanUsers
from keyboards import inline_keyboards as ikb
from libs.config import id_admin


@dp.callback_query_handler(Text(startswith='support_'))
async def call_support(call: types.CallbackQuery, state: FSMContext):
    with DB() as db:
        get_ban_list = db.give_is_ban_users(call.message.chat.id)
        if get_ban_list:
            get_info_ban = db.give_ban_info_user(call.message.chat.id)
            await call.message.edit_text(f'<b>Вы были заблокированы!\n\nПричина:</b> <i>{get_info_ban[1]}</i>')
            await state.finish()
            return
    
    await state.set_state(Support.id_user)
    
    await call.message.edit_text('<b>Напишите свое сообщение прямо в этот чат 👇</b>', reply_markup=ikb.cancel_support())


@dp.message_handler(state=Support.id_user)
async def support_handler(message: types.Message, state: FSMContext):
    try:
        await bot.delete_message(message.chat.id, message_id=message.message_id-1)
    except aiogram.utils.exceptions.MessageToDeleteNotFound:
        pass
    
    if len(message.text) > 1000:
        return await message.answer('<b>Опишите свою проблему сообщением более кратком и понятном виде, не более 1000 символов:</b>', reply_markup=ikb.cancel_support())

    for i in id_admin():
        try:
            await bot.send_message(i,   f'<b>tag_id:</b> <code>#{message.message_id}</code>\n'   
                                        f'<b>Пользователь:</b> {message.from_user.full_name}\n'
                                        f'<b>UserName:</b> @{message.from_user.username}\n'
                                        f'<b>ID:</b> <code>{message.from_user.id}</code>\n\n'
                                        f'<b>Сообщение:</b> {message.text}'.replace('@None', 'Скрыт'), reply_markup=ikb.reply_message_in_support(message.chat.id))
        except:
            pass

    await message.answer('<b>Ваше сообщение было доставлено Администраторам</b>', reply_markup=ikb.main_menu_panel_markup())
    await state.finish()


@dp.callback_query_handler(Text(startswith='admin_to_ask_'))
async def call_admin_to_ask_support(call: types.CallbackQuery, state: FSMContext):
    call_msg = call.data.split('_')

    await state.set_state(ToAskAdmin.id_user)

    async with state.proxy() as data:
        data['id_user'] = int(call_msg[3])

    await call.message.answer('Введите сообщение для пользователя', reply_markup=ikb.cancel_reply_message_for_users())


@dp.callback_query_handler(Text(startswith='admin_notify_'))
async def call_admin_notify_support(call: types.CallbackQuery, state: FSMContext):
    call_msg = call.data.split('_')
    print(call_msg)
    await state.set_state(NotifyAdmin.id_user)

    async with state.proxy() as data:
        data['id_user'] = int(call_msg[2])

    await call.message.answer(f'Введите сообщение для пользователя <u>что-бы его Известить</u>', reply_markup=ikb.cancel_reply_message_for_users())


@dp.callback_query_handler(Text(startswith='set_ban_'))
async def call_admin_notify_support(call: types.CallbackQuery, state: FSMContext):
    call_msg = call.data.split('_')
    
    if int(call_msg[2]) not in id_admin():    
        await state.set_state(SetInfoBanUsers.id_user)

        async with state.proxy() as data:
            data['id_user'] = int(call_msg[2])

        return await call.message.answer(f'<b>Пришлите причину Бана пользователя ID</b> <code>{call_msg[2]}</code>'
                                         '<b>максимум 800 символов или пришлите "-" что-бы оставить описание причины Бана Пустым</b>', reply_markup=ikb.cancel_reply_message_for_users())
            
    if id_admin()[0] == call.message.chat.id:
        return await call.message.answer('<b>Возможно этот пользователь Администратор!</b>\n-Вы можете управлять Администраторами в разделе Админка->Админы')

    await call.message.answer(f'<b>Возможно этот пользователь Администратор!</b>\n-Вы НЕ можете управлять Администраторами, сообщите Главному Администратору по ID <code>{id_admin()[0]}</code> в поддержке')


@dp.callback_query_handler(Text(startswith='reply_message_user_in_support_close_id_'))
async def call_admin_notify_support(call: types.CallbackQuery):
    call_msg = call.data.split('_')
    
    await call.message.delete()

    try:
        await bot.send_message(int(call_msg[7]), text='<b>Пользователь закрыл диалог c вами</b>')
    except:
        pass    


@dp.callback_query_handler(Text(startswith='users_to_ask_'))
async def call_admin_to_ask_support(call: types.CallbackQuery, state: FSMContext):
    call_msg = call.data.split('_')
    await state.set_state(ToAskUsers.id_admin)

    async with state.proxy() as data:
        data['id_admin'] = int(call_msg[3])

    await call.message.answer(f'<b>Введите сообщение</b>', reply_markup=ikb.cancel_reply_message_for_users())


@dp.callback_query_handler(Text(startswith='users_thank_'))
async def call_admin_notify_support(call: types.CallbackQuery):
    _id_admin = int(call.data.split('_')[2])

    await call.message.edit_text('<b>Спасибо!</b>')
    
    message_text = '<b>Вас только что Поблагодарил пользователь за Вашу Обратную связь</b>\n\n'
    with DB() as db:
        get_karma_admins = db.сharacteristic_bot()

        if get_karma_admins[0][11] != 0:
            old_karama_admin = db.give_karma_admin(_id_admin)

            main_admin = id_admin()
            if _id_admin == main_admin[0]:
                message_text += f'<b>Главному Администратору не нужна карма, если хотите его добавить себе то напишите разработчику @ProgramsCreator</b>'

            if old_karama_admin is not None:
                db.update_karma_admin(_id_admin, get_karma_admins[0][11], old_karama_admin[0])
                message_text += f'<b>Ваша карма увеличилась на:</b> +{get_karma_admins[0][11]}'
    
    try:
        await bot.send_message(_id_admin, message_text)
    except:
        pass


@dp.message_handler(state=ToAskAdmin.id_user)
async def call_reply_message_user(message: types.Message, state: FSMContext):
    
    async with state.proxy() as data:
        _id_user = data['id_user']

    await reply_message_func(message, _id_user, 'to_ask')
    await state.finish()


@dp.message_handler(state=ToAskUsers.id_admin)
async def call_reply_message_user(message: types.Message, state: FSMContext):
    if len(message.text) > 1000:
        return await message.answer('<b>Опишите свою проблему сообщением более кратком и понятном виде, не более 1000 символов:</b>', reply_markup=ikb.cancel_support())

    async with state.proxy() as data:
        _id_admin = data['id_admin']

    await reply_message_func(message, _id_admin, 'users_to_ask')
    await state.finish()


@dp.message_handler(state=NotifyAdmin.id_user)
async def call_reply_message_user(message: types.Message, state: FSMContext):
    
    async with state.proxy() as data:
        _id_user = data['id_user']


    await reply_message_func(message, _id_user, 'notify')
    await state.finish()


@dp.message_handler(state=SetInfoBanUsers.id_user)
async def call_reply_message_user(message: types.Message, state: FSMContext):

    if len(message.text) > 800:
        return await message.answer('<b>Максимум 800 символов в описании причины Бана пользователя или пришлите "-" что-бы оставить описание причины Бана Пустым:</b>')

    async with state.proxy() as data:
        _id_user = data['id_user']
    
    msg_user_ban = '<b>Вы были заблокированы Администрацией!</b>'
    msg_admin_ban = '<b>Пользователь Заблокирован 🔴!</b>'
    with DB() as db:
        db.update_ban_list('ban', _id_user, message.text)

        if message.text != '-':    
            msg_user_ban += f'\n\n<b>Причина Бана:</b> <i>{message.text}</i>'
            msg_admin_ban += msg_user_ban

    try:
        await bot.send_message(_id_user, msg_user_ban)
    except:
        pass
    
    await state.finish()
    await message.answer(f'<b>Пользователь Заблокирован 🔴!</b>\n\nПричина Бана: <i>{message.text}</i>')


async def reply_message_func(message: types.Message, _id, method):
    try:
        if method == 'to_ask':
            await bot.send_message(_id, f'<b>Админ</b>\n{message.text}', reply_markup=ikb.reply_message_user_in_support(message.from_user.id))
        elif method == 'notify':
            await bot.send_message(_id, f'<b>Админ</b>\n{message.text}')
    except:
        return await message.answer(f'<b>Не получилось доставить ответное сообщение Пользователю: {_id}</b>')
        
    if method == 'users_to_ask':
        try:
            await bot.send_message(_id, f'<b>Пользователь:</b> {message.from_user.full_name}\n'
                                        f'<b>UserName:</b> @{message.from_user.username}\n'
                                        f'<b>ID:</b> <code>{message.from_user.id}</code>\n\n'
                                        f'<b>Сообщение:</b> {message.text}'.replace('@None', 'Скрыт'), reply_markup=ikb.reply_message_in_support(message.chat.id))
        except:
            await message.answer('Не получилось доставить сообщение Администратору который держал с вами связь\nОбратитесь снова в раздел Поддержка для привлечения помощи других Админов')

    await message.answer('<b>Сообщение отправлено</b>')


