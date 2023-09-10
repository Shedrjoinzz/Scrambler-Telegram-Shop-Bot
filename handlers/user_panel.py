from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from libs.config import id_admin

from data.db import DB

def user_panel(id_users):
    with DB() as db:
        select_is_basket = db.give_basket_products_all(id_users)

    basket_msg = 'Корзина 🗑'
    if [] != select_is_basket:
        basket_msg = 'Корзина 🟢'
    markup = InlineKeyboardMarkup()
    in1 = InlineKeyboardButton(text='Каталоги 🗂', callback_data='catalog_s')
    in2 = InlineKeyboardButton(text=basket_msg, callback_data='basketgiveproducts_')
    in3 = InlineKeyboardButton(text='Профиль 🖥', callback_data='profile_')
    in4 = InlineKeyboardButton(text='FAQ ♨️', callback_data='faq_')
    in5 = InlineKeyboardButton(text='Поддержка 👨🏼‍💻', callback_data='support_')
    markup.add(in1, in2)
    markup.add(in3)
    markup.add(in4, in5)
    if id_users in id_admin():
        in6 = InlineKeyboardButton(text='Админка 🔐', callback_data='admin_')
        markup.add(in6)
    return markup