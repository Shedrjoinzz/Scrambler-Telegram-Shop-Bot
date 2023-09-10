import aiogram
from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.storage import FSMContext
from aiogram.utils.exceptions import CantParseEntities

import asyncio

from keyboards import inline_keyboards as ikb
from data.db import DB
from loader import dp, bot
from states.state import SetCharacteristic
from handlers import commands as com

@dp.callback_query_handler(Text(startswith='management_bot_admin_'))
async def call_management_bot_admin(call: types.CallbackQuery, state: FSMContext):
    await one_message_in_manager_bot(call)
    

@dp.callback_query_handler(Text(startswith='manager_bot_edit_'))
async def call_manager_bot_edit(call: types.CallbackQuery, state: FSMContext):
    call_msg = int(call.data.split('_')[3])

    await state.set_state(SetCharacteristic.id_call_msg)

    async with state.proxy() as data:
        data['id_call_msg'] = call_msg
    set_msg = '<b>Доступные теги:</b>\n<code>%first_name%</code> - Имя пользователя\n<code>%username%</code> - Никнейм пользователя\n<code>%user_id%</code> - ID пользователя\n<code>%datetime%</code> - Покажет дату И время <b>00-00-00дмг 00:00:00чмс</b>\n\n<b>Доступна HTML разметка</b>'
    if call_msg == 1:
        await call.message.edit_text(f'Введите сообщение которое будет показана пользователям после покупки товара, максимум 300 символов или введите "-" что-бы оставить системное сообщение\n\n{set_msg}',
                                     reply_markup=ikb.cancel_edits_manager_bot())
    
    if call_msg == 2:
        await call.message.edit_text(f'Введите сообщение которое будет показана пользователям после нажатия команды СТАРТ <code>/start</code>, максимум 900 символов или введите "-" что-бы оставить системное сообщение\n\n{set_msg}',
                                     reply_markup=ikb.cancel_edits_manager_bot())

    if call_msg == 3:
        await call.message.edit_text('Введите сумму МАКСИМАЛЬНОГО пополнения баланса RUB или введите "0" что-бы задать пустым',
                                     reply_markup=ikb.cancel_edits_manager_bot())

    if call_msg == 4:
        await call.message.edit_text('Введите сумму МИНИМАЛЬНОГО пополнения баланса RUB или введите "0" что-бы задать пустым',
                                     reply_markup=ikb.cancel_edits_manager_bot())
        
    if call_msg == 5:
        await call.message.edit_text(f'Введите сообщение которое будет показана НОВЫМ пользователям после нажатия /start или введите "-" что-бы оставить системное сообщение\n\n{set_msg}',
                                     reply_markup=ikb.cancel_edits_manager_bot())
        
    if call_msg == 6:
        await call.message.edit_text(f'Введите сообщение которое будет показана в разделе FAQ или введите "-" что-бы оставить пустым, максимум 1900 символов\n\n{set_msg}',
                                     reply_markup=ikb.cancel_edits_manager_bot())
        
    if call_msg == 7:
        await call.message.edit_text(f'Введите сообщение, которое будет показано пользователю в случае, если Админ включил Режим Обслуживания или введите "-" что-бы оставить системное сообщение, максимум 500 символов\n\n{set_msg}',
                                     reply_markup=ikb.cancel_edits_manager_bot())

    if call_msg == 8:
        await call.message.edit_text('Введите Реферальное Вознаграждение в RUB или введите "0" что-бы <b>Отключить</b> реферальное вознаграждение:',
                                     reply_markup=ikb.cancel_edits_manager_bot())
    
    if call_msg == 9:
        await call.message.edit_text('Введите Реферальное Вознаграждение (в Процентах) без "%" или введите "0" что-бы <b>Отключить</b> реферальное вознаграждение:',
                                     reply_markup=ikb.cancel_edits_manager_bot())

    if call_msg == 10:
        await call.message.edit_text('Введите карму Администраторам максимум 1000 или введите "0" что-бы <b>Отключить</b>\n\n'
                                     '-<b>Карма</b> это оценка Администраторов за их обратную связь с пользователями\n\n'
                                     '-<b>Пользователи</b> могут Отблагодарить Администратора (который был на связи с юзером) за качественную обратную связь при этом увиличив Карму самому Администратору',
                                     reply_markup=ikb.cancel_edits_manager_bot())

@dp.message_handler(state=SetCharacteristic.id_call_msg)
async def set_characteristic(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        get_id_call_msg = data['id_call_msg']

    with DB() as db:

        if get_id_call_msg == 1:

            if len(message.text) > 300:
                try:
                    await bot.delete_message(message.chat.id, message_id=message.message_id-1)
                except aiogram.utils.exceptions.MessageToDeleteNotFound:
                    pass
                await message.answer(f'Не более 300 символов!\nВ вашем: {len(message.text)} символов',
                                     reply_markup=ikb.cancel_edits_manager_bot())
                return

            if message.text == '-':
                try:
                    await bot.delete_message(message.chat.id, message_id=message.message_id-1)
                except aiogram.utils.exceptions.MessageToDeleteNotFound:
                    pass
                db.update_сharacteristic_bot('str', 'message_is_buy_product', '-')
                await message.answer('Установлено системное сообщение после покупки товара',
                                     reply_markup=ikb.back_to_manager_bot())
                await state.finish()
                return
            
            is_false = await parse_error_exceptions(message)

            if is_false == False:
                return
            
            try:
                await bot.delete_message(message.chat.id, message_id=message.message_id-1)
            except aiogram.utils.exceptions.MessageToDeleteNotFound:
                pass
            db.update_сharacteristic_bot('str', 'message_is_buy_product', f'{message.text}')
            await message.answer('Изменения успешно сохранены', reply_markup=ikb.back_to_manager_bot())
            await state.finish()


        if get_id_call_msg == 2:

            if len(message.text) > 900:
                try:
                    await bot.delete_message(message.chat.id, message_id=message.message_id-1)
                except aiogram.utils.exceptions.MessageToDeleteNotFound:
                    pass
                await message.answer(f'Не более 900 символов!\nВ вашем: {len(message.text)} символов',
                                     reply_markup=ikb.cancel_edits_manager_bot())
                return

            if message.text == '-':
                try:
                    await bot.delete_message(message.chat.id, message_id=message.message_id-1)
                except aiogram.utils.exceptions.MessageToDeleteNotFound:
                    pass
                db.update_сharacteristic_bot('str', 'message_is_start', '-')
                await message.answer('Установлено системное сообщение после команды /start',
                                     reply_markup=ikb.back_to_manager_bot())
                await state.finish()
                return

            is_false = await parse_error_exceptions(message)

            if is_false == False:
                return

            try:
                await bot.delete_message(message.chat.id, message_id=message.message_id-1)
            except aiogram.utils.exceptions.MessageToDeleteNotFound:
                pass
            db.update_сharacteristic_bot('str', 'message_is_start', f'{message.text}')
            await message.answer('Изменения успешно сохранены',
                                 reply_markup=ikb.back_to_manager_bot())
            await state.finish()


        if get_id_call_msg == 5:

            if len(message.text) > 900:
                try:
                    await bot.delete_message(message.chat.id, message_id=message.message_id-1)
                except aiogram.utils.exceptions.MessageToDeleteNotFound:
                    pass
                await message.answer(f'Не более 900 символов!\nВ вашем: {len(message.text)} символов',
                                     reply_markup=ikb.cancel_edits_manager_bot())
                return


            if message.text == '-':
                try:
                    await bot.delete_message(message.chat.id, message_id=message.message_id-1)
                except aiogram.utils.exceptions.MessageToDeleteNotFound:
                    pass
                db.update_сharacteristic_bot('str', 'message_is_new_user', '-')
                await message.answer('Установлено <b>системное сообщение</b> НОВЫМ пользователям!',
                                     reply_markup=ikb.back_to_manager_bot())
                await state.finish()
                return
            
            is_false = await parse_error_exceptions(message)

            if is_false == False:
                return
            
            try:
                await bot.delete_message(message.chat.id, message_id=message.message_id-1)
            except aiogram.utils.exceptions.MessageToDeleteNotFound:
                pass
            db.update_сharacteristic_bot('str', 'message_is_new_user', f'{message.text}')
            await message.answer('Изменения успешно сохранены',
                                 reply_markup=ikb.back_to_manager_bot())
            
            await state.finish()


        if get_id_call_msg == 6:

            if len(message.text) > 1900:
                try:
                    await bot.delete_message(message.chat.id, message_id=message.message_id-1)
                except aiogram.utils.exceptions.MessageToDeleteNotFound:
                    pass
                await message.answer(f'Не более 1900 символов!\nВ вашем: {len(message.text)} символов',
                                     reply_markup=ikb.cancel_edits_manager_bot())
                return


            if message.text == '-':
                try:
                    await bot.delete_message(message.chat.id, message_id=message.message_id-1)
                except aiogram.utils.exceptions.MessageToDeleteNotFound:
                    pass
                await message.answer('Раздел FAQ пользователям задано <b>пустым!</b>',
                                     reply_markup=ikb.back_to_manager_bot())
                db.update_сharacteristic_bot('str', 'message_is_faq', '-')
                await state.finish()
                return
            
            is_false = await parse_error_exceptions(message)

            if is_false == False:
                
                return
            
            try:
                await bot.delete_message(message.chat.id, message_id=message.message_id-1)
            except aiogram.utils.exceptions.MessageToDeleteNotFound:
                pass
            db.update_сharacteristic_bot('str', 'message_is_faq', f'{message.text}')
            await message.answer('Изменения успешно сохранены',
                                 reply_markup=ikb.back_to_manager_bot())
            
            await state.finish()


        if get_id_call_msg == 7:
            
            if len(message.text) > 500:
                try:
                    await bot.delete_message(message.chat.id, message_id=message.message_id-1)
                except aiogram.utils.exceptions.MessageToDeleteNotFound:
                    pass
                await message.answer(f'<b>Ваще сообщение содержит {len(message.text)} символов\nМаксимум 500:</b>')
                return
            
            if message.text == '-':
                try:
                    await bot.delete_message(message.chat.id, message_id=message.message_id-1)
                except aiogram.utils.exceptions.MessageToDeleteNotFound:
                    pass
                db.update_сharacteristic_bot('str', 'service_bot_message', message.text)
                await message.answer('<b>Установлено системное сообщение!</b>')
                await state.finish()
                return

            is_false = await parse_error_exceptions(message)

            if is_false == False:
                return
            
            try:
                await bot.delete_message(message.chat.id, message_id=message.message_id-1)
            except aiogram.utils.exceptions.MessageToDeleteNotFound:
                pass
            db.update_сharacteristic_bot('str', 'service_bot_message', message.text)
            await message.answer('Изменения успешно сохранены',
                                 reply_markup=ikb.back_to_manager_bot())
            await state.finish()
            

        if get_id_call_msg == 8:
            try:
                _value = float(message.text)
            except ValueError:
                await bot.delete_message(message.chat.id, message_id=message.message_id-1)
                await message.answer('Введите число!', reply_markup=ikb.cancel_edits_manager_bot())
                return
            except aiogram.utils.exceptions.MessageToDeleteNotFound:
                pass

            if _value < 0:
                try:
                    await bot.delete_message(message.chat.id, message_id=message.message_id-1)
                except aiogram.utils.exceptions.MessageToDeleteNotFound:
                    pass
                await message.answer('Реферальное Вознаграждение не может быть отрицательным числом!',
                                    reply_markup=ikb.cancel_edits_manager_bot())
                return
            
            if _value > 1_000_000:
                try:
                    await bot.delete_message(message.chat.id, message_id=message.message_id-1)
                except aiogram.utils.exceptions.MessageToDeleteNotFound:
                    pass
                await bot.delete_message(message.chat.id, message_id=message.message_id-1)
                await message.answer('Слишком шедрое Реферальное Вознаграждение! :)',
                                    reply_markup=ikb.cancel_edits_manager_bot())
                return
            
            if _value == 0:
                try:
                    await bot.delete_message(message.chat.id, message_id=message.message_id-1)
                except aiogram.utils.exceptions.MessageToDeleteNotFound:
                    pass
                db.update_сharacteristic_bot('int', 'ref_summ', 0)
                await message.answer('Реферально Вознаграждение <b>Отключено</b>!',
                                        reply_markup=ikb.back_to_manager_bot())
                await state.finish()
                return
            try:
                await bot.delete_message(message.chat.id, message_id=message.message_id-1)
            except aiogram.utils.exceptions.MessageToDeleteNotFound:
                pass

            db.update_сharacteristic_bot('int', 'ref_summ', _value)
            await message.answer(f'Реферально Вознаграждение задано <b>{_value} RUB</b>!',
                                    reply_markup=ikb.back_to_manager_bot())
            await state.finish()
        

        if get_id_call_msg == 9:
            try:
                _value = float(message.text)
            except ValueError:
                await bot.delete_message(message.chat.id, message_id=message.message_id-1)
                await message.answer('Введите число!', reply_markup=ikb.cancel_edits_manager_bot())
                return
            except aiogram.utils.exceptions.MessageToDeleteNotFound:
                pass

            if _value < 0:
                try:
                    await bot.delete_message(message.chat.id, message_id=message.message_id-1)
                except aiogram.utils.exceptions.MessageToDeleteNotFound:
                    pass
                await message.answer('Реферальное Вознаграждение (в Процентах) не может быть отрицательным числом!',
                                    reply_markup=ikb.cancel_edits_manager_bot())
                return
            
            if _value > 100:
                try:
                    await bot.delete_message(message.chat.id, message_id=message.message_id-1)
                except aiogram.utils.exceptions.MessageToDeleteNotFound:
                    pass
                await message.answer('Реферальное Вознаграждение (в Процентах) не может быть больше 100%!',
                                    reply_markup=ikb.cancel_edits_manager_bot())
                return
            
            if _value == 0:
                try:
                    await bot.delete_message(message.chat.id, message_id=message.message_id-1)
                except aiogram.utils.exceptions.MessageToDeleteNotFound:
                    pass
                db.update_сharacteristic_bot('int', 'ref_procent_top_up', 0)
                await message.answer('Реферально Вознаграждение (в Процентах) <b>Отключено</b>!',
                                        reply_markup=ikb.back_to_manager_bot())
                await state.finish()
                return
            
            try:
                await bot.delete_message(message.chat.id, message_id=message.message_id-1)
            except aiogram.utils.exceptions.MessageToDeleteNotFound:
                pass
            db.update_сharacteristic_bot('float', 'ref_procent_top_up', _value)
            await message.answer(f'Реферальное Вознаграждение (в Процентах) задано <b>{_value}%</b>!',
                                    reply_markup=ikb.back_to_manager_bot())
            await state.finish()
        

        if get_id_call_msg == 10:
            try:
                _value = int(message.text)

            except ValueError:
                try:
                    await bot.delete_message(message.chat.id, message_id=message.message_id-1)
                except aiogram.utils.exceptions.MessageToDeleteNotFound:
                    pass
                await message.answer('Введите число!', reply_markup=ikb.cancel_edits_manager_bot())
                return
            
            if _value > 1000:
                try:
                    await bot.delete_message(message.chat.id, message_id=message.message_id-1)
                except aiogram.utils.exceptions.MessageToDeleteNotFound:
                    pass
                return await message.answer('Максимальная карма для Администраторов 1000!',
                                     reply_markup=ikb.cancel_edits_manager_bot())
                

            if _value < 0:
                try:
                    await bot.delete_message(message.chat.id, message_id=message.message_id-1)
                except aiogram.utils.exceptions.MessageToDeleteNotFound:
                    pass

                return await message.answer('Карма не может быть отрицательным!',
                                            reply_markup=ikb.cancel_edits_manager_bot())

            if _value == 0:
                try:
                    await bot.delete_message(message.chat.id, message_id=message.message_id-1)
                except aiogram.utils.exceptions.MessageToDeleteNotFound:
                    pass
                db.update_сharacteristic_bot('int', 'karma', 0)
                await message.answer('Карма Администраторов <b>Отключена</b>!',
                                        reply_markup=ikb.back_to_manager_bot())
            
                await state.finish()
                return
            
            try:
                await bot.delete_message(message.chat.id, message_id=message.message_id-1)
            except aiogram.utils.exceptions.MessageToDeleteNotFound:
                pass
            db.update_сharacteristic_bot('int', 'karma', _value)
            await message.answer(f'Карма Администраторов установлено {_value}!',
                                    reply_markup=ikb.back_to_manager_bot())
        
            await state.finish()
            return
            
        if get_id_call_msg == 3 or get_id_call_msg == 4:
            try:
                _value = int(message.text)

            except ValueError:
                await bot.delete_message(message.chat.id, message_id=message.message_id-1)
                await message.answer('Введите число!', reply_markup=ikb.cancel_edits_manager_bot())
                return
            except aiogram.utils.exceptions.MessageToDeleteNotFound:
                pass

                   
            if get_id_call_msg == 3:
                
                if _value > 1_000_000:
                    try:
                        await bot.delete_message(message.chat.id, message_id=message.message_id-1)
                    except aiogram.utils.exceptions.MessageToDeleteNotFound:
                        pass
                    await message.answer('МАКСИМАЛЬНОЕ пополнение не может превышать <b>1 000 000 RUB</b>!',
                                    reply_markup=ikb.cancel_edits_manager_bot())
                    return
                
                if _value == 0:
                    try:
                        await bot.delete_message(message.chat.id, message_id=message.message_id-1)
                    except aiogram.utils.exceptions.MessageToDeleteNotFound:
                        pass
                    db.update_сharacteristic_bot('int', 'max_summ_top_up', 0)
                    await message.answer('МАКСИМАЛЬНОЕ пополнение задано <b>пустым</b>!',
                                            reply_markup=ikb.back_to_manager_bot())
                    return

                try:
                    await bot.delete_message(message.chat.id, message_id=message.message_id-1)
                except aiogram.utils.exceptions.MessageToDeleteNotFound:
                    pass
                db.update_сharacteristic_bot('int', 'max_summ_top_up', _value)
                await message.answer(f'МАКСИМАЛЬНОЕ пополнение задано {_value} RUB!',
                                        reply_markup=ikb.back_to_manager_bot())

            if get_id_call_msg == 4:
                get_max_summ = db.give_max_and_min_summ()
                if get_max_summ[0] != 0:
                    if _value >= get_max_summ[0]:
                        await message.answer('МИНИМАЛЬНОЕ пополнение не может быть больше или равен текущему МАКСИМАЛЬНОМУ значение!',
                                    reply_markup=ikb.cancel_edits_manager_bot())
                        return

                if _value < 0:
                    await message.answer('МИНИМАЛЬНОЕ пополнение не может быть отрицательным числом!',
                                    reply_markup=ikb.cancel_edits_manager_bot())
                    return

                if _value < 9 and _value != 0:
                    await message.answer('МИНИМАЛЬНОЕ пополнение не должен быть меньше 10 RUB\nТакие условия у платёжной системы PayMaster')
                    return
                
                if _value == 0:
                    db.update_сharacteristic_bot('int', 'min_summ_top_up', 10)
                    await message.answer('МИНИМАЛЬНОЕ пополнение задано <b>по условиям PayMaster</b>!',
                                            reply_markup=ikb.back_to_manager_bot())
                    return


                db.update_сharacteristic_bot('int', 'min_summ_top_up', _value)
                await message.answer(f'МИНИМАЛЬНОЕ пополнение задано {_value} RUB!',
                                        reply_markup=ikb.back_to_manager_bot())

            await state.finish()

        
@dp.callback_query_handler(Text(startswith='cancel_state_edit_manager_bot_'), state=SetCharacteristic.id_call_msg)
async def cancel_state_edit_manager_bot(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await one_message_in_manager_bot(call)


async def one_message_in_manager_bot(call: types.CallbackQuery):
    with DB() as db:
        get_all_сharacteristic = db.сharacteristic_bot()

    status_captcha = f'{get_all_сharacteristic[0][8]}'.replace('0', '<code>Отключено</code>').replace('1', '<code>Включено </code>\n     ┗Режим Защиты 1.ур Выбор Цифры').replace('2', '<code>Включено</code>\n     ┗Режим Защиты 2.ур Ввод Цифр').replace('3', '<b>Включено</b>\n     ┗Режим Защиты 3.ур Решение Уровнений')

    len_msg = f'''<b>Здесь Вы можете управлять некоторыми функциями магазина, вот настройки магазина на данный момент:</b>\n\n
<b>1) Сообщение после покупки:</b> <code>{get_all_сharacteristic[0][0][:100] + '...'}</code>

<b>2) Сообщение после команды</b> СТАРТ: <code>{get_all_сharacteristic[0][1][:100] + '...'}</code>

<b>3) Максимальная сумма пополнения:</b> <b>{get_all_сharacteristic[0][4]}</b> RUB

<b>4) МИНИМАЛЬНАЯ сумма пополнения:</b> <b>{get_all_сharacteristic[0][5]}</b> RUB

<b>5) Сообщение новым пользователям:</b> <code>{get_all_сharacteristic[0][2][:100] + '...'}</code>

<b>6) FAQ Магазина:</b> <code>{get_all_сharacteristic[0][6][:200] + '...'}</code>

<b>7) Сообщение об Обслуживании Бота:</b> <code>{get_all_сharacteristic[0][7][:100] + '...'}</code>

<b>8) Реферальное вознаграждение:</b> {get_all_сharacteristic[0][9]} RUB | {get_all_сharacteristic[0][10]}%

<b>9) ┣Защита Бота:</b> {status_captcha}

<b>10) Карма Администраторов: {get_all_сharacteristic[0][11]}</b>'''
    
    await call.message.edit_text(len_msg, reply_markup=ikb.select_menu_in_manager_bot())

    await com.delete_all_message_chat(call.message)



@dp.callback_query_handler(text='select_type_anti_bot')
async def call_select_type_anti_bot(call: types.CallbackQuery):
    await call.message.edit_text('<b>Выберите способ Защиты бота</b>\n\n'
                                 '<b>Выбор Цифры</b> - Новый пользователь должен выбрать правильную цифру рандом от 1 до 5\n\n'
                                 '<b>Ввод Чисел</b> - Новый пользователь должен ввести рандомное число которое изображено на картине\n\n'
                                 '<b>Решение задачи</b> - Новый пользователь должен решить задачу на (сложение, вычитание, умножение)', reply_markup=ikb.select_method_captcha_bot())
    
@dp.callback_query_handler(text='select_edit_ref_system')
async def call_select_type_anti_bot(call: types.CallbackQuery):
    await call.message.edit_text('<b>Выберите что хотите изменить</b>', reply_markup=ikb.select_edit_type_ref_system())



async def parse_error_exceptions(message: types.Message):
    try:
        await message.answer(f'Установлено: {message.text}')
    except CantParseEntities:
        get_id = await message.answer('<b>В вашем сообщении не правильно прописаны <u>теги HTML</u></b>\nИправьте или отправьте сообщение без HTML разметки')
        await asyncio.sleep(5)
        try:
            await bot.delete_message(message.chat.id, message_id=get_id.message_id)
        except aiogram.utils.exceptions.MessageToDeleteNotFound:
            pass
        return False
