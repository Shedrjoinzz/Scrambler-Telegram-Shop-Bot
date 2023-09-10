import aiogram
from aiogram import types
from aiogram.dispatcher.storage import FSMContext
from aiogram.dispatcher.filters import Text

from data.db import DB
from loader import dp, bot
from states.state import MessengerAdmin, MessengerUser
from keyboards import inline_keyboards as ikb

@dp.callback_query_handler(Text(startswith='message_for_'))
async def call_message_for(call: types.CallbackQuery, state: FSMContext):
    await state.set_state(MessengerAdmin.id_user)
    
    await call.message.edit_text('<b>Пришлите ID пользователя которому хотите отправить сообщение</b>', reply_markup=ikb.exit_from_messenger())

@dp.message_handler(state=MessengerAdmin.id_user)
async def call_get_id_user(message: types.Message, state: FSMContext):

    try:
        int_id_user = int(message.text)
        
        with DB() as db:
            get_is_id = db.give_id_user(int_id_user)
            
        if message.chat.id != int_id_user:
            if get_is_id is not None:
                async with state.proxy() as data:
                    data['id_user'] = int_id_user

                await message.answer(f'Пришлите сообщение которое хотите отправить пользователю,\nМаксимум 2000 символов или нажмите <b>"Отмена"</b> если передумали', reply_markup=ikb.exit_from_messenger())
                await state.set_state(MessengerAdmin.message_user)
            else:
                await message.answer('<b>Нет такого пользователя в базе</b>', reply_markup=ikb.exit_from_messenger())
        else:
            await message.answer('<b>Нельзя отправить сообщение самому себе\nПришлите ID пользователя</b>', reply_markup=ikb.exit_from_messenger())            

    except ValueError:
        await message.answer('<b>Пришлите ID!</b>', reply_markup=ikb.exit_from_messenger())

@dp.message_handler(state=MessengerAdmin.message_user)
async def message_for_user(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        _id_user = data['id_user']
    try:
        if len(message.text) > 2000:
            await message.answer('<b>Ощибка</b>\n'
                                 f'Максимум символов: 2000\n'
                                 f'В вашем сообщении: {len(message.text)}', reply_markup=ikb.exit_from_messenger())
            return
        
        await bot.send_message(_id_user, f"<b>Сообщение от Админа</b>\n\n{message.text}", reply_markup=ikb.reply_message_admin_or_user('admin', message.chat.id))
        await message.answer('Сообщение успешно доставлено!')
        await state.finish()
    except:
        await message.answer(f'Ощибка\nНе удалось доставить сообщение, возможно пользователь {_id_user} заблокировал бота')
        await state.finish()


@dp.callback_query_handler(Text(startswith='reply_'))
async def call_reply_admin_message(call: types.CallbackQuery, state: FSMContext):
    call_msg = call.data.split('_')

    await state.set_state(MessengerUser.id)

    async with state.proxy() as data:
        data['id'] = int(call_msg[3])
        data['method'] = call_msg[1]

    await call.message.edit_text('<b>Отправьте ответ\nНе более 900 символов</b>', reply_markup=ikb.exit_from_messenger())


@dp.message_handler(state=MessengerUser.id)
async def message_for_admin(message: types.Message, state: FSMContext):
    try:
        await bot.delete_message(message.chat.id, message_id=message.message_id)
    except aiogram.utils.exceptions.MessageToDeleteNotFound:
        pass
    if len(message.text) > 900:
        await message.answer('<b>Ощибка</b>\n'
                                f'Максимум символов: 900\n'
                                f'В вашем сообщении: {len(message.text)}', reply_markup=ikb.exit_from_messenger())
        return

    async with state.proxy() as data:
        _id = data['id']
        _method = data['method']
        
    if _method == 'admin':
        await bot.send_message(_id, 'Сообщение от пользователя\n'
                                        f'<b>ID:</b> <code>{message.chat.id}</code>\n'
                                        f'<b>UserName:</b> @{message.from_user.username}\n'
                                        f'<b>FullName:</b> {message.from_user.full_name}\n'
                                        f'<b>TEXT:</b>\n\n{message.text}'.replace("@None", "Нет Юзера"),
                                        reply_markup=ikb.reply_message_admin_or_user('user', message.chat.id))
    
    elif _method == 'user':
        try:
            await bot.send_message(_id, '<b>Сообщение от Админа</b>\n\n'
                                        f'{message.text}', reply_markup=ikb.reply_message_admin_or_user('admin', message.chat.id))
        except Exception:
            await message.answer('<b>Ощибка</b>\nНе удалось доставить сообщение', reply_markup=ikb.main_menu_panel_markup())
            await state.finish()

    await message.answer('Сообщение успешно было отправлено', reply_markup=ikb.main_menu_panel_markup())
    await state.finish()
        
