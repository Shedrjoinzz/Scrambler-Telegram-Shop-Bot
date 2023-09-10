from aiogram import types
from aiogram.dispatcher.filters import Text

from datetime import datetime

from loader import dp
from keyboards import inline_keyboards as ikb
from data.db import DB

@dp.callback_query_handler(Text(startswith='buyprductsinbasket_'))
async def call_buy_product(call: types.CallbackQuery):
    call_msg = call.data.split('_')
    print(call_msg)
    await call.message.edit_text('Нажимая "Купить" Вы соглашаетесь с правилами магазина которые описаны в разделе FAQ на главном меню.', reply_markup=ikb.success_or_cancel(call_msg[5], call_msg[1], call_msg[2]))

@dp.callback_query_handler(Text(startswith='buy_product_in_basket_'))
async def call_buy_product_in_basket(call: types.CallbackQuery):
    call_msg = call.data.split('_')

    with DB() as db:
        get_ban_list = db.give_is_ban_users(call.message.chat.id)
        if get_ban_list:
            get_info_ban = db.give_ban_info_user(call.message.chat.id)
            return await call.message.edit_text(f'<b>Вы были заблокированы!\n\nПричина:</b> <i>{get_info_ban[1]}</i>')

        
        get_balance_user = db.give_info_user('balance_rub', call.message.chat.id)
        get_info_product = db.give_info_product(call_msg[4])
        get_count_product = db.give_basket_product(call.message.chat.id, call_msg[4])


    if get_balance_user[0] >= float(call_msg[8]):

        if get_info_product[0][5] < 0:
            return await call.message.answer('Товар НЕ был куплен!\n'
                                              '<b>Возможно купили последний :(</b>', reply_markup=ikb.back_in_main_menu())
            
        
        if get_info_product[0][5] < int(call_msg[6]):
            return await call.message.answer('<b>Выбранное количество товара больше чем товаров в базе</b>\n'
                                            'Удалены некоторые товары в которых количество товара добавленные в корзину превышало количество в базе\n'
                                            '<u>Возможно пользователи скупили больщую часть товара</u>\n\n'
                                            '[?] Данное действие выполняется автоматически\n')

        db.basket_isBuyProduct(call.message.chat.id, call_msg[4], get_info_product[0][5], call_msg[6], int(get_balance_user[0])-int(call_msg[8]))

        give_product_user = ''
        try:
            for i in range(1, int(get_count_product[0][3])+1):
                give_product_user += f'{i}) <code>{get_info_product[0][6]}</code>\n'
        except IndexError:
            pass

        await call.message.answer(f'{give_product_user}')

        get_msg_isBuyProduct = db.give_all_msg_in_data()

        if get_msg_isBuyProduct[0] != '-':
            date_time_str = str(datetime.now()).split(".")[0]
            
            return await call.message.answer(f'{get_msg_isBuyProduct[0]}'.replace("%first_name%", call.from_user.first_name).replace("%username%", call.from_user.username).replace("%user_id%", f"{call.from_user.id}").replace("%datetime%", date_time_str))
            

        return await call.message.answer('<b>Спасибо за покупку!</b>', reply_markup=ikb.back_in_main_menu())
        
    else:
        await call.message.answer('<b>У вас не достаточно средств!</b>', reply_markup=ikb.user_profile_and_back_menu())

