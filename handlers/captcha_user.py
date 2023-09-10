from aiogram import types
import aiogram
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.storage import FSMContext

from random import randint
import asyncio

from loader import dp, bot
from data.db import DB 
from handlers import user_panel as uikb
from keyboards import inline_keyboards as ikb
from states.state import AntiUsersBotSecurityNumbers, AntiUsersBotSecurityPhotoNumbers, AntiUsersBotSecuritySolvingEquations
from .commands import generate_captcha_photo, delete_all_message_chat, generate_captcha_expression, add_referal_bonus, notify_new_user

@dp.callback_query_handler(Text(startswith='captcha_number_'), state=AntiUsersBotSecurityNumbers.number)    
async def captcha_number_user(call: types.CallbackQuery, state: FSMContext):
    call_msg = call.data.split('_')

    if call_msg[2] != call_msg[3]:
        _number = randint(1, 5)

        await call.message.edit_text(f'Не правильно! Была цифра {call_msg[3]}\n'
                                     '<b>Рещите капчу</b>\n'
                                     f'Нажмите на цифру: <b>{_number}</b>', reply_markup=ikb.captcha_users(_number, call_msg[4]))
        return
    
    await state.finish()

    with DB() as db:
        await add_referal_bonus(call.message, call_msg[4])
        get_start_message = db.give_message_is_start_and_message_is_buy_and_status_bot_and_captcha()
        db.add_new_user(call.from_user.id, 0, 0, call.from_user.first_name, call.from_user.last_name, call.from_user.username, call.from_user.language_code, 0)
        await notify_new_user(call.message, call.message.chat.id)

    if get_start_message[2] != '-':
        await call.message.edit_text(f'{get_start_message[2]}'.replace("%first_name%", call.from_user.first_name).replace("%username%", call.from_user.username).replace("%user_id%", f"{call.from_user.id}"))
        return

    await call.message.edit_text('<b>Добро пожаловать!</b>', reply_markup=uikb.user_panel(call.from_user.id))


@dp.message_handler(state=AntiUsersBotSecurityPhotoNumbers.photo_number)
async def call_user_enter_photo_captcha(message: types.Message, state: FSMContext):
    try:
        _int_enter = int(message.text)
    except:
        _id = await message.answer('Введите цифры которые показаны на изображении')
        await asyncio.sleep(3)
        try:
            await bot.delete_message(message.chat.id, message_id=message.message_id)
        except aiogram.utils.exceptions.MessageToDeleteNotFound:
            pass

        return
    
    async with state.proxy() as data:
        _rand_number = data['photo_number']
        _id_ref = data['id_ref']

    if _rand_number != _int_enter:
        await delete_all_message_chat(message)
        rand_number = randint(10000, 1000000)

        async with state.proxy() as data:
            data['photo_number'] = rand_number
            
        await generate_captcha_photo(rand_number)
        
        await asyncio.sleep(1)
        
        with open('handlers/headers/ImgCaptcha_output/CAPTCHA.png', 'rb') as img:
            await message.answer_photo(img, caption='Не правильно!\n<b>Отправьте цифры которые изображены на картинке</b>', reply_markup=ikb.update_photo_captcha_users())
        return
    
    await add_referal_bonus(message, _id_ref)    
    await state.finish()
    await delete_all_message_chat(message)

    with DB() as db:
        get_start_message = db.give_message_is_start_and_message_is_buy_and_status_bot_and_captcha()
        db.add_new_user(message.from_user.id, 0, 0, message.from_user.first_name, message.from_user.last_name, message.from_user.username, message.from_user.language_code, 0)
        await notify_new_user(message, message.chat.id)

    if get_start_message[2] != '-':
        await message.answer(f'{get_start_message[2]}'.replace("%first_name%", message.from_user.first_name).replace("%username%", message.from_user.username).replace("%user_id%", f"{message.from_user.id}"))
        return

    await message.answer('<b>Добро пожаловать!</b>', reply_markup=uikb.user_panel(message.chat.id))

 

@dp.callback_query_handler(Text(startswith='update_catpcha'), state=AntiUsersBotSecurityPhotoNumbers.photo_number)
async def call_update_catpcha(call: types.CallbackQuery, state: FSMContext):
    rand_number = randint(10000, 1000000)

    async with state.proxy() as data:
        data['photo_number'] = rand_number

    await generate_captcha_photo(rand_number)

    with open('handlers/headers/ImgCaptcha_output/CAPTCHA.png', 'rb') as img:
        photo = types.InputMediaPhoto(img, caption="<b>Отправьте цифры которые изображены на картинке</b>")
        await bot.edit_message_media(chat_id=call.message.chat.id, message_id=call.message.message_id, media=photo, reply_markup=ikb.update_photo_captcha_users())


@dp.message_handler(state=AntiUsersBotSecuritySolvingEquations.answer)
async def result_expression_user(message: types.Message, state: FSMContext):

    async with state.proxy() as data:
        _answer = data['answer']
        _id_ref = data['id_ref']

    if message.text != str(_answer[3]):
        get_list_value = await generate_captcha_expression()

        async with state.proxy() as data:
            data['answer'] = get_list_value
            data['id_ref'] = _id_ref

        await message.answer('Не верно!\n'
                            f'<b>Решите уровнение:</b> {get_list_value[0]} {get_list_value[1]} {get_list_value[2]} = ?')
        return

    await add_referal_bonus(message, _id_ref)            
    await state.finish()
    
    with DB() as db:
        get_start_message = db.give_message_is_start_and_message_is_buy_and_status_bot_and_captcha()
        db.add_new_user(message.from_user.id, 0, 0, message.from_user.first_name, message.from_user.last_name, message.from_user.username, message.from_user.language_code, 0)
        await notify_new_user(message, message.chat.id)

    if get_start_message[2] != '-':
        await message.answer(f'{get_start_message[2]}'.replace("%first_name%", message.from_user.first_name).replace("%username%", message.from_user.username).replace("%user_id%", f"{message.from_user.id}"))
        return

    await message.answer('<b>Добро пожаловать!</b>', reply_markup=uikb.user_panel(message.chat.id))
    await delete_all_message_chat(message)