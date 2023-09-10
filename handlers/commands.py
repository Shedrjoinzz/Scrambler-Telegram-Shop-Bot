from aiogram import types
import aiogram
from aiogram.dispatcher.storage import FSMContext

from datetime import datetime
from captcha.image import ImageCaptcha
from random import randint, choices

from loader import dp, bot
from data.db import DB 
from handlers import user_panel as uikb
from keyboards import inline_keyboards as ikb
from libs import config
from states.state import AntiUsersBotSecurityNumbers, AntiUsersBotSecurityPhotoNumbers, AntiUsersBotSecuritySolvingEquations

@dp.message_handler(commands='start')
async def start_handlers(message: types.Message, state: FSMContext):
    with DB() as db:
        get_ban_list = db.give_is_ban_users(message.chat.id)
        if get_ban_list:
            get_info_ban = db.give_ban_info_user(message.chat.id)
            return await message.answer(f'<b>Вы были заблокированы!\n\nПричина:</b> <i>{get_info_ban[1]}</i>')

    date_time_str = str(datetime.now()).split(".")[0]

    id_user = db.give_id_user(message.from_user.id)
    print(id_user)
    get_system_message = db.give_message_is_start_and_message_is_buy_and_status_bot_and_captcha()

    if get_system_message == False or get_system_message == None:
        db.add_is_not_add_basic_value_in_db()
        try:
            for i in config.id_admin():
                await bot.send_message(i, '<b>АДМИНАМ:</b>\nДополнительные данные внесены в базу!\nОтправьте ещё раз: /start')
        except:
            pass
        return
    
    if not message.chat.id in config.id_admin():
        
        if get_system_message[3] is False:
            if get_system_message[4] != '-':
                return await message.answer(f'{get_system_message[4]}'.replace("%first_name%", message.from_user.first_name).replace("%username%", message.from_user.username).replace("%user_id%", f"{message.from_user.id}").replace("%datetime%", date_time_str))
                    
            return await message.answer('<b>Бот находится на тех.обслуживании\n\nЕсли Вы Админ перейдите в раздел\nАдминка->Бот->Обслуживание</b>')
            
    
    
    if id_user == None:
        if get_system_message[5] == 1:
            await state.set_state(AntiUsersBotSecurityNumbers.number)
            _number = randint(1, 5)
            return await message.answer('Рещите капчу\n'
                                f'Нажмите на цифру: <b>{_number}</b>', reply_markup=ikb.captcha_users(_number, message.text[7:]))
            
        if get_system_message[5] == 2:
            await state.set_state(AntiUsersBotSecurityPhotoNumbers.photo_number)
            rand_number = randint(10000, 1000000)
            await generate_captcha_photo(rand_number)

            async with state.proxy() as data:
                data['photo_number'] = rand_number
                data['id_ref'] = message.text[7:]

            with open('handlers/headers/ImgCaptcha_output/CAPTCHA.png', 'rb') as img:
                await message.answer_photo(img, '<b>Отправьте цифры которые изображены на картинке</b>', reply_markup=ikb.update_photo_captcha_users())
            return

        if get_system_message[5] == 3:
            await state.set_state(AntiUsersBotSecuritySolvingEquations.answer)

            get_list_value = await generate_captcha_expression()
            
            async with state.proxy() as data:
                data['answer'] = get_list_value
                data['id_ref'] = message.text[7:]

                
            return await message.answer(f'<b>Решите уровнение:</b> {get_list_value[0]} {get_list_value[1]} {get_list_value[2]} = ?')

        await add_referal_bonus(message, message.text[7:])

        db.add_new_user(message.from_user.id, 0, 0, message.from_user.first_name, message.from_user.last_name, message.from_user.username, message.from_user.language_code, 0)
        
        await notify_new_user(message, message.chat.id)
 
        if get_system_message[2] != '-':
            await message.answer(f'{get_system_message[2]}'.replace("%first_name%", message.from_user.first_name).replace("%username%", message.from_user.username).replace("%user_id%", f"{message.from_user.id}").replace("%datetime%", date_time_str))
            return

        await message.answer('Добро пожаловать!', reply_markup=uikb.user_panel(message.chat.id))
        return
    
    if get_system_message[0] != '-':
        await message.answer(f'{get_system_message[0]}'.replace("%first_name%", message.from_user.first_name).replace("%username%", message.from_user.username).replace("%user_id%", f"{message.from_user.id}").replace("%datetime%", date_time_str),
                            reply_markup=uikb.user_panel(message.chat.id))
        
        await delete_all_message_chat(message)
        return

    await message.answer(f'Главное меню', reply_markup=uikb.user_panel(message.chat.id))
    await delete_all_message_chat(message)



async def generate_captcha_expression():
    rand_number_one = randint(3, 30)
    rand_expression = choices('+-*', k=1)        
    rand_number_two = randint(2, 20)
    answer = eval(f'{rand_number_one} {rand_expression[0]} {rand_number_two}')

    list = [rand_number_one, rand_expression[0], rand_number_two, answer]
    return list
    

async def generate_captcha_photo(rand_number):
    image = ImageCaptcha(width = 300, height = 120)

    image.generate(f'{rand_number}')

    image.write(f'{rand_number}', 'handlers/headers/ImgCaptcha_output/CAPTCHA.png')


async def add_referal_bonus(message: types.Message, start_message):        
    with DB() as db:
        try:
            _id_ref = int(start_message)
        except ValueError:
            db.add_ref_system(message.chat.id, 0)
            return

        if _id_ref == '':
            db.add_ref_system(message.chat.id, 0)
            return

        select_user_ref = db.give_id_user(_id_ref)

        if select_user_ref is None:
            db.add_ref_system(message.chat.id, 0)
            return

        if _id_ref == message.chat.id:
            db.add_ref_system(message.chat.id, 0)
            return
        
        if _id_ref != '':

            get_is_ref_id = db.give_id_ref_users(message.chat.id)

            if get_is_ref_id:
                db.add_ref_system(message.chat.id, _id_ref)
                get_old_balance_run_and_procent = db.give_info_user('balance_rub, procent', _id_ref)
                get_bonus_procent_and_balance_rub = db.сharacteristic_bot()
                db.add_bonus_ref(_id_ref, get_old_balance_run_and_procent[0], get_old_balance_run_and_procent[1], float(get_bonus_procent_and_balance_rub[0][9]), float(get_bonus_procent_and_balance_rub[0][10]))
                
                try:
                    await bot.send_message(_id_ref, '<b>У вас новый Реферал!</b>\n'
                                                    f'<b>FullName:</b> {message.from_user.full_name}\n'
                                                    f'<b>UserName: @{message.from_user.username}</b>'.replace('@None', '<i>Отсутвтует</i>'))
                except:
                    pass
                return

            db.add_ref_system(message.chat.id, 0)
            return
                
async def notify_new_user(message: types.Message, id_user):
    try:
        for i in config.id_admin():
            if i == id_user:
                return
            await bot.send_message(i, '<b>Новый пользователь:</b>\n'
                                        f'<b>ID:</b> <code>{message.from_user.id}</code>\n'
                                        f'<b>FullName:</b> {message.from_user.full_name}\n'
                                        f'<b>UserName</b> @{message.from_user.username}'.replace('@None', 'Отсутствует'))
    except:
        pass


async def delete_all_message_chat(message: types.Message):
    try:
        for i in range(1, message.message_id):
            await bot.delete_message(message.from_user.id, message_id=message.message_id-i)
    except aiogram.utils.exceptions.MessageToDeleteNotFound:
        pass

