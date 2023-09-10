from aiogram import types

from keyboards import inline_keyboards as ikb
from data.db import DB
from loader import dp
from libs.config import id_admin, USERNAME_BOT

@dp.callback_query_handler(text='profile_')
async def call_profile(call: types.CallbackQuery):
    isAdmin = id_admin()
    with DB() as db:
        get_all_product_in_basket = db.give_basket_products_all(call.message.chat.id)
        get_all_info_from_user = db.give_info_user('*', call.message.chat.id)
        get_conut_all_ref_users = db.give_count_ref_users_profile(call.message.chat.id)
        get_my_ref_id = db.give_user_ref_id(call.message.chat.id)

        my_ref_text = "<b>Вас пригласил:</b> <u>Сам пришёл</u>"
        if get_my_ref_id[0] != 0:
            my_ref_info = db.give_info_user('name, username', get_my_ref_id[0])
            my_ref_text = f"<b>Вас пригласил:</b> {my_ref_info[0]} @{my_ref_info[1]}".replace('@None', '<u>Отсутствует</u>')
        
        message_text = (f"<b>Ваш профиль</b> 📱\n\n"
                        f"🆔: <code>{call.message.chat.id}</code>\n"
                        f"🪪 <b>FullName:</b> {call.from_user.full_name}\n"
                        f"♐️ <b>UserName:</b> {call.from_user.username}\n"
                        f"👤 {my_ref_text}\n"
                        f"👥 <b>Рефералы:</b> {get_conut_all_ref_users[0][0]}\n"
                        f"💰 <b>Баланс:</b> {get_all_info_from_user[2]} <b>RUB</b> \n"
                        f"🗑 <b>Товаров в корзине:</b> {len(get_all_product_in_basket)}\n"
                        f"⚖️ <b>Процент на пополнение:</b> {get_all_info_from_user[3]}% <b>(один раз)</b>\n\n"
                        f"🔗 <b>Ваша реферальная ссылка: https://t.me/{USERNAME_BOT.replace('@', '')}?start={call.message.chat.id}</b>")
        
        if call.message.chat.id in isAdmin:
            getIndexAdmin = isAdmin.index(call.message.chat.id)
            get_karma = db.give_karma_admin(isAdmin[getIndexAdmin])
            if get_karma is not None:
                message_text += (f"\n\n<b>Статус Админ</b> ✅\n"
                                 f"🔮 Карма: {get_karma[0]}")

    await call.message.edit_text(message_text, reply_markup=ikb.user_profile_and_back_menu())
    

