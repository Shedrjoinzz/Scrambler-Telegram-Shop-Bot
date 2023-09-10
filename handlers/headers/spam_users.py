import aiogram
from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.storage import FSMContext

from states.state import SpamUsers
from keyboards import inline_keyboards as ikb
from loader import dp, bot
from data.db import DB
from handlers import commands as com
from keyboards import admin_keyboards as aikb

import html

@dp.callback_query_handler(text='spam_users_admin_')
async def call_spam_users(call: types.CallbackQuery, state: FSMContext):
    await state.set_state(SpamUsers._message)
    await call.message.edit_text("Пришлите пост к рассылке:", reply_markup=ikb.cancel_spam_to_users())

@dp.message_handler(state=SpamUsers._message)
async def select_count_spam_users(message: types.Message, state: FSMContext):
    quote_message = message.text

    if len(quote_message) <= 2000:
        try:
            await message.answer('<b>Готово к рассылке:</b>\n\n'
                                f'{quote_message}')
            
        except aiogram.utils.exceptions.CantParseEntities:
            
            quote_message = html.escape(message.text, quote=None)

            await message.answer('<b>Готово к рассылке:</b>\n\n'
                                f'{quote_message}')

        async with state.proxy() as data:
            data['_message'] = quote_message

        
        await state.set_state(SpamUsers._save_message)
        return await message.answer('Выще ваше сообщение которое будет отправлено пользователям\n\nНажмите "<b>Запуск</b>" для начала рассылки или "<b>Отмена</b>" если передумали',
                                    reply_markup=ikb.select_count_spam_users())
    
    await message.answer(f'Ваш текст содержит {len(message.text)} символов, допустимое кол-во символов в сообщении 2000\n\n<b>Пришлите пост к рассылке</b>',
                            reply_markup=ikb.cancel_spam_to_users())


@dp.callback_query_handler(Text(startswith='start_spam_'), state=SpamUsers._save_message)
async def call_get_count_spam_users(call: types.CallbackQuery, state: FSMContext):
    try:
        await bot.delete_message(call.message.chat.id, message_id=call.message.message_id)
    except aiogram.utils.exceptions.MessageToDeleteNotFound:
        pass

    try:
        async with state.proxy() as data:
            _message = data['_message']
        with DB() as db:
            id_users = db.get_count_users_in_spam()
        for i in id_users:
            await bot.send_message(i[0], _message)
        if i[0] == id_users[len(id_users)-1][0]:
            await call.message.answer('Рассылка заверщена')
        
        await state.finish()
    except Exception:
        pass

@dp.callback_query_handler(Text(startswith='cancel_spam_'), state=SpamUsers)
async def call_cancel_spam(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.edit_text('Рассылка отменена', reply_markup=aikb.main_admin_panel())
    await com.delete_all_message_chat(call.message)

