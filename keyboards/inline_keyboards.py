from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def give_category(category, db, isTrue = True):
    markup_category = InlineKeyboardMarkup()
    for _i in category:
        gets = db.give_all_product_in_catalogs(_i[0])
        if isTrue:
            setText = f'{_i[1]} | 🟢'
            if [] == gets:
                setText = f'{_i[1]} | 🗑'
        else:
            setText = _i[1]
        markup_category.row(InlineKeyboardButton(text=setText, callback_data=f'catalog_{_i[0]}'))
    markup_category.row(InlineKeyboardButton(text='Главное Меню 🔝', callback_data='back_menu'))
    return markup_category

def give_product_in_catalog(method, id_catalog, product):
    markup_product = InlineKeyboardMarkup()
    setData = f'catalog_{id_catalog}'
    if method == 'delete_':
        setData = 'delete_products_'
        if product != []:
            markup_product.row(InlineKeyboardButton(text='Удалить всё ❌', callback_data=f'{method}all_product_{id_catalog}'))

    for i in product:
        setText = i[2]
        if method == 'edits_':
            setText = f'{i[2]} ✏️'
            setData = 'edit_old_product_admin_'
        elif method == 'delete_':
            setText = f'{i[2]} ❌'
        elif i[5] != 0:
            setText += ' 🟢'
        elif i[5] == 0:
            setText += ' 🗑'
        markup_product.row(InlineKeyboardButton(text=setText, callback_data=f'{method}product_{i[0]}_{id_catalog}'))
    markup_product.row(InlineKeyboardButton(text='⬅️ Назад', callback_data=setData),
                        InlineKeyboardButton(text='Главное Меню 🔝', callback_data='back_menu'))
    return markup_product

def back_list_product(id_catalog, id_products, isProduct = False):
    markup_lvl_product = InlineKeyboardMarkup()
    _callback_data = f"CountInBasket_select_{id_products}"
    if '0' != id_products:
        if isProduct:
            _callback_data = f"isProduct_{id_products}"
        markup_lvl_product.add(InlineKeyboardButton(text='В Корзину ➕', callback_data=_callback_data))
    markup_lvl_product.row(InlineKeyboardButton(text='⬅️ Назад', callback_data=f'catalog_{id_catalog}'),
                            InlineKeyboardButton(text='Главное Меню 🔝', callback_data='back_menu'))
    return markup_lvl_product

def back_list_catalog():
    markup_lvl_product = InlineKeyboardMarkup()
    markup_lvl_product.row(InlineKeyboardButton(text='⬅️ Назад', callback_data='catalog_s'),
                            InlineKeyboardButton(text='Главное Меню 🔝', callback_data='back_menu'))
    return markup_lvl_product

def give_basket_products(id_product, db):
    markup_basket = InlineKeyboardMarkup()
    print(id_product)
    for _id in id_product:
        # print(_id)
        info = db.give_info_product(_id[1])
        # print(len(info))
        if info[0][5] == 0:
            db.delete_product_in_basket(_id[0], _id[1])

        if info != []:
            _summ = float(info[0][4]) * float(_id[3])
            print(_id[3])
            markup_basket.row(InlineKeyboardButton(text=f'{info[0][2]}', callback_data=f'isProduct_{_id[1]}'),
                            InlineKeyboardButton(text=f'💳 Оплатить {_summ}', callback_data=f'buyprductsinbasket_{_id[3]}_{int(_summ)}_i_i_{info[0][0]}')) # 'buyprductsinbasket_{_id[3]}_{int(_summ)}_{info[0][6]}_{info[0][5]}_{info[0][0]}'
    markup_basket.row(InlineKeyboardButton(text='Главное Меню 🔝', callback_data='back_menu'))
    return markup_basket

def back_menu_or_cancel_operation():
    cancel = InlineKeyboardMarkup()
    cancel.row(InlineKeyboardButton(text='Отмена 🚫', callback_data=f'cancel_'))
    return cancel

def basket_product_menu(id_user, id_product, name_product, count_in_basket, max_count_product):
    markup_basket = InlineKeyboardMarkup()
    in1 = InlineKeyboardButton(text='Изменить кол-во ✏️', callback_data=f'EditBasketProduct_{id_user}_{id_product}_name_{count_in_basket}_{max_count_product}')
    in2 = InlineKeyboardButton(text='Удалить товар ❌', callback_data=f'DelBasketProduct_{id_user}_{id_product}_{name_product}')
    markup_basket.add(in1, in2)
    markup_basket.row(InlineKeyboardButton(text='⬅️ Назад', callback_data='basketgiveproducts_'),
                            InlineKeyboardButton(text='Главное Меню 🔝', callback_data='back_menu'))
    return markup_basket

def back_basket_list(method):
    basket = InlineKeyboardMarkup()
    if method == 'basketgiveproducts_':
        basket.row(InlineKeyboardButton(text='⬅️ Назад', callback_data='basketgiveproducts_'))
    if method != 'basketgiveproducts_' and method == 'back_menu':
        basket.row(InlineKeyboardButton(text='⬅️ Назад', callback_data='back_menu'))
    return basket

# (🗑🚫✳️🛂💬❌❇️📊👥🔐📝📲🖥💾🔝💳🔎🔰🔢 🧮📱🟢🟠⚖️💸🙏✅❕✏️)

def multi_give_count(method, count_product):
    multi_give = InlineKeyboardMarkup(row_width = 2)
    for i in range(1, int(count_product)+1):
        _callback_data = f'pressCount_{i}'
        _backdata = 'add_count_product_cancel'
        if 40 >= int(count_product):
            if method == 'edit':
                _callback_data = f'pressEditCount_{i}'
                _backdata = 'EditCountInBasket_cancel'
            multi_give.row(InlineKeyboardButton(text=f'{i}', callback_data=_callback_data))
    multi_give.row(InlineKeyboardButton(text='Отмена 🚫', callback_data=_backdata))
    return multi_give
    
def edit_basket_count(id_product, count, method):
    edit_markup = InlineKeyboardMarkup()
    in1 = InlineKeyboardButton(text='Готово', callback_data=f'basket_{id_product}_{count}_{method}')
    in2 = InlineKeyboardButton(text='Отмена 🚫', callback_data='EditCountInBasket_close')
    edit_markup.add(in1)
    edit_markup.add(in2)
    return edit_markup

def add_basket_count(id_product, count, method):
    add_markup = InlineKeyboardMarkup()
    in1 = InlineKeyboardButton(text='Готово', callback_data=f'basket_{id_product}_{count}_{method}')
    in2 = InlineKeyboardButton(text='Отмена 🚫', callback_data='AddCountInBasket_close')
    add_markup.add(in1)
    add_markup.add(in2)
    return add_markup

def success_or_cancel(id_basket_product, count_product, price_basket_product):
    markup_dialog = InlineKeyboardMarkup()
    markup_dialog.row(InlineKeyboardButton(text='Купить', callback_data=f'buy_product_in_basket_{id_basket_product}_count_{count_product}_price_{price_basket_product}'),
                      InlineKeyboardButton(text='Отмена 🚫', callback_data='basketgiveproducts_'))
    return markup_dialog

def success_button(method):
    markup_success = InlineKeyboardMarkup()
    if method == '1':
        markup_success.row(InlineKeyboardButton(text='Сохранить 💾', callback_data=f'add_success_{method}'))
    markup_success.row(InlineKeyboardButton(text='Отмена 🚫', callback_data=f'add_catalog_cancel'))
    return markup_success

def multi_control_category(category, db, method, _type, isTrue = True):
    markup_category = InlineKeyboardMarkup()
    _back_data = 'admin_'
    if category != []:
        if _type == 'delete_product' or _type == 'delete_catalog':
            _type = _type.split('_')[1]

            if _type == 'catalog':
                markup_category.row(InlineKeyboardButton(text='Удалить всё ❌', callback_data=f'{method}_all_{_type}_'))
    for _i in category:
        gets = db.give_all_product_in_catalogs(_i[0])
        if _type == 'catalog':
            if isTrue:
                setText = f'{_i[1]} 🟢 ❌'
                if [] == gets:
                    setText = f'{_i[1]} 🗑 ❌'
            
            else:
                setText = _i[1]
        if _type == 'product':
            _back_data = 'admin_'
            if method == 'add':
                _back_data = 'cancel_product_advanced'
            if isTrue:
                setText = f'{_i[1]} 🟢'
                if [] == gets:
                    setText = f'{_i[1]} 🗑'
            else:
                setText = _i[1]
        markup_category.row(InlineKeyboardButton(text=setText, callback_data=f'{method}_{_type}_{_i[0]}'))
    markup_category.row(InlineKeyboardButton(text='⬅️ Назад', callback_data=_back_data))
    return markup_category

def success_delete_catalog(id_catalog):
    markup_delete = InlineKeyboardMarkup()
    markup_delete.row(InlineKeyboardButton(text='Удалить ❌', callback_data=f'successfully_delete_catalog_{id_catalog}'),
                      InlineKeyboardButton(text='Отмена 🚫', callback_data='cancel_delete_'))
    return markup_delete

def select_count_spam_users():
    markup_select_spam = InlineKeyboardMarkup()
    markup_select_spam.row(InlineKeyboardButton(text='Запустить', callback_data='start_spam_'),
                           InlineKeyboardButton(text='Отмена 🚫', callback_data='cancel_spam_'))
    return markup_select_spam

def cance_add_new_product(): # так надо 
    markup_cancel_add = InlineKeyboardMarkup()
    markup_cancel_add.row(InlineKeyboardButton(text='Отмена 🚫', callback_data='cancel_add_new_product'))
    return markup_cancel_add

def user_profile_and_back_menu():
    markup_user_profile = InlineKeyboardMarkup()
    in1 = InlineKeyboardButton(text='Пополнить Баланс', callback_data='top_up_balance_')
    in2 = InlineKeyboardButton(text='⬅️ Назад', callback_data='back_menu')
    markup_user_profile.add(in1)
    markup_user_profile.add(in2)
    return markup_user_profile

def select_top_up_balance():
    markup_select_top_up = InlineKeyboardMarkup()
    in1 = InlineKeyboardButton(text='PayMaster', callback_data='paymaster_')
    in2 = InlineKeyboardButton(text='⬅️ Назад', callback_data='profile_')
    markup_select_top_up.add(in1)
    markup_select_top_up.add(in2)
    return markup_select_top_up


def select_menu_in_manager_bot():
    marktup_menu_in_manager_bot = InlineKeyboardMarkup(row_width=3)        
    in1 = InlineKeyboardButton(text='Изменить 1', callback_data='manager_bot_edit_1')
    in2 = InlineKeyboardButton(text='Изменить 2', callback_data='manager_bot_edit_2')
    in3 = InlineKeyboardButton(text='Изменить 3', callback_data='manager_bot_edit_3')
    in4 = InlineKeyboardButton(text='Изменить 4', callback_data='manager_bot_edit_4')
    in5 = InlineKeyboardButton(text='Изменить 5', callback_data='manager_bot_edit_5')
    in6 = InlineKeyboardButton(text='Изменить 6', callback_data='manager_bot_edit_6')
    in7 = InlineKeyboardButton(text='Изменить 7', callback_data='manager_bot_edit_7')
    in8 = InlineKeyboardButton(text='Изменить 8', callback_data='select_edit_ref_system')
    in9 = InlineKeyboardButton(text='Изменить 9', callback_data='select_type_anti_bot')
    in10 = InlineKeyboardButton(text='Изменить 10', callback_data='manager_bot_edit_10')
    in11 = InlineKeyboardButton(text='Админка', callback_data='admin_')
    marktup_menu_in_manager_bot.add(in1, in2)
    marktup_menu_in_manager_bot.add(in3, in4)
    marktup_menu_in_manager_bot.add(in5, in6)
    marktup_menu_in_manager_bot.add(in7, in8)
    marktup_menu_in_manager_bot.add(in9, in10)
    marktup_menu_in_manager_bot.add(in11)
    return marktup_menu_in_manager_bot

def cancel_edits_manager_bot():
    markup_cancel_state_to_manager_bot = InlineKeyboardMarkup()
    markup_cancel_state_to_manager_bot.row(InlineKeyboardButton(text='Отмена 🚫', callback_data='cancel_state_edit_manager_bot_'))
    return markup_cancel_state_to_manager_bot

def back_to_manager_bot():
    markup_back_manager_bot = InlineKeyboardMarkup()
    markup_back_manager_bot.row(InlineKeyboardButton(text='Бот', callback_data='management_bot_admin_'))
    return markup_back_manager_bot

def cancel_spam_to_users():
    markup_cancel_user_spam = InlineKeyboardMarkup()
    markup_cancel_user_spam.row(InlineKeyboardButton(text='Отмена 🚫', callback_data='cancel_spam_'))
    return markup_cancel_user_spam

def exit_from_messenger():
    markup_exit_messenger = InlineKeyboardMarkup()
    markup_exit_messenger.row(InlineKeyboardButton(text='Отмена 🚫', callback_data=f'exit_from_messenger_'))
    return markup_exit_messenger

def reply_message_admin_or_user(method, _id):
    markup_reply_message = InlineKeyboardMarkup()
    markup_reply_message.row(InlineKeyboardButton(text='Ответить', callback_data=f'reply_{method}_message_{_id}'))
    return markup_reply_message

def main_menu_panel_markup():
    markup_main_menu = InlineKeyboardMarkup()
    markup_main_menu.row(InlineKeyboardButton(text='Главное Меню 🔝', callback_data='back_menu'))
    return markup_main_menu

def select_add_product():
    markup_select_add_product = InlineKeyboardMarkup(row_width=1)
    markup_select_add_product.row(InlineKeyboardButton(text='Обычный', callback_data='select_add_product_usual'),
                                  InlineKeyboardButton(text='Продвинутый', callback_data='select_add_product_advanced'))
    markup_select_add_product.row(InlineKeyboardButton(text='⬅️ Назад', callback_data='admin_'))
    return markup_select_add_product

def select_add_or_cancel_product(method=False):
    markup_select_add_or_cancel_product = InlineKeyboardMarkup()
    if method == True:
        markup_select_add_or_cancel_product.row(InlineKeyboardButton(text='Добавить', callback_data='add_product_advanced'))
    markup_select_add_or_cancel_product.row(InlineKeyboardButton(text='Отмена 🚫', callback_data='cancel_product_advanced'))
    return markup_select_add_or_cancel_product

def select_edit_element_in_product(id_product):
    markup_edit_element = InlineKeyboardMarkup()
    in1 = InlineKeyboardButton(text='Изменить ✏️1', callback_data=f'one_old_edit_product_1_{id_product}')
    in2 = InlineKeyboardButton(text='Изменить ✏️2', callback_data=f'one_old_edit_product_2_{id_product}')
    in3 = InlineKeyboardButton(text='Изменить ✏️3', callback_data=f'one_old_edit_product_3_{id_product}')
    in4 = InlineKeyboardButton(text='Изменить ✏️4', callback_data=f'one_old_edit_product_4_{id_product}')
    in5 = InlineKeyboardButton(text='Изменить ✏️5', callback_data=f'one_old_edit_product_5_{id_product}')
    in6 = InlineKeyboardButton(text='Админка', callback_data='admin_')
    markup_edit_element.add(in1, in2)
    markup_edit_element.add(in3, in4)
    markup_edit_element.add(in5)
    markup_edit_element.add(in6)
    return markup_edit_element

def cancel_edit_one_product():
    markup_cancel_edit_one_product = InlineKeyboardMarkup()
    markup_cancel_edit_one_product.row(InlineKeyboardButton(text='Отмена 🚫', callback_data='cancel_edit_one_product'))
    return markup_cancel_edit_one_product

def cancel_support():
    markup_cancel_edit_one_product = InlineKeyboardMarkup()
    markup_cancel_edit_one_product.row(InlineKeyboardButton(text='Отмена 🚫', callback_data='cancel_support'))
    return markup_cancel_edit_one_product

def back_in_main_menu():
    markup_back_main_menu_user = InlineKeyboardMarkup()
    markup_back_main_menu_user.row(InlineKeyboardButton(text='⬅️ Назад', callback_data='back_menu'))
    return markup_back_main_menu_user

def cancel_top_up_balance():
    markup_cancel_top_up_balance = InlineKeyboardMarkup()
    markup_cancel_top_up_balance.row(InlineKeyboardButton(text='Отмена 🚫', callback_data='cancel_top_up_balance_user'))
    return markup_cancel_top_up_balance
    
def back_in_admin_menu():
    markup_back_in_admin_menu = InlineKeyboardMarkup()
    markup_back_in_admin_menu.row(InlineKeyboardButton(text='⬅️ Назад', callback_data='admin_'))
    return markup_back_in_admin_menu

def select_users_manager():
    markup_select_manager_users = InlineKeyboardMarkup()
    in1 = InlineKeyboardButton(text='Информация 🔎', callback_data='info_user')
    in2 = InlineKeyboardButton(text='Данные 💾', callback_data='get_all_info_excel')
    in3 = InlineKeyboardButton(text='Процент пополнения 📝 (все)', callback_data='edit_procent_all_users')
    in4 = InlineKeyboardButton(text='Заблокировать 💢 (все)', callback_data='ban_all_users')
    in5 = InlineKeyboardButton(text='Разблокировать ✅ (все)', callback_data='unban_all_users')
    in6 = InlineKeyboardButton(text='⬅️ Назад', callback_data='admin_')
    markup_select_manager_users.add(in1, in2)
    markup_select_manager_users.add(in3)
    markup_select_manager_users.add(in4, in5)
    markup_select_manager_users.add(in6)
    return markup_select_manager_users

def select_one_user_manager(_id_user):
    markup_one_user_manager = InlineKeyboardMarkup()
    in1 = InlineKeyboardButton(text='Изменить Баланс ✏️', callback_data='edit_balance_user')
    in2 = InlineKeyboardButton(text='Изменить Процент ✏️', callback_data='edit_procent_user')
    in3 = InlineKeyboardButton(text='Заблокировать 💢', callback_data='edit_status_user_ban')
    in4 = InlineKeyboardButton(text='Разблокировать ✅', callback_data='edit_status_user_unban')
    in5 = InlineKeyboardButton(text='Сообщение 💬', callback_data='push_msg_one_user')
    in6 = InlineKeyboardButton(text='Назначить 👮‍♂️', callback_data=f'add_in_admin_id_{_id_user}')
    in7 = InlineKeyboardButton(text='⬅️ Назад', callback_data='cancel_info_user')
    markup_one_user_manager.add(in1, in2)
    markup_one_user_manager.add(in3, in4)
    markup_one_user_manager.add(in5, in6)
    markup_one_user_manager.add(in7)
    return markup_one_user_manager

def cancel_method(method):
    markup_method = InlineKeyboardMarkup()
    markup_method.row(InlineKeyboardButton(text='Отмена 🚫', callback_data=f'{method}'))
    return markup_method

def user_edit_button():
    markup_user_edit_back_button = InlineKeyboardMarkup()
    markup_user_edit_back_button.row(InlineKeyboardButton(text='⬅️ Назад', callback_data='info_user'),
                                     InlineKeyboardButton(text='Главное Меню 🔝', callback_data='back_menu'))
    return markup_user_edit_back_button


def export_data_shop():
    markup_export_data = InlineKeyboardMarkup()
    in1 = InlineKeyboardButton(text='🔰 Экспорт Таблицы (users)', callback_data='export_users')
    in2 = InlineKeyboardButton(text='🔰 Экспорт Таблицы (admins)', callback_data='export_admins')
    in3 = InlineKeyboardButton(text='🔰 Экспорт Таблицы (ban_list)', callback_data='export_ban_list')
    in4 = InlineKeyboardButton(text='🔰 Экспорт Таблицы (catalogs)', callback_data='export_catalogs')
    in5 = InlineKeyboardButton(text='🔰 Экспорт Таблицы (products)',callback_data='export_products')
    in6 = InlineKeyboardButton(text='🔰 Экспорт Таблицы (basket)',callback_data='export_basket')
    in7 = InlineKeyboardButton(text='🔰 Экспорт Таблицы (manager_bot)',callback_data='export_manager_bot')
    in8 = InlineKeyboardButton(text='🔰 Экспорт Таблицы (statistic_finance)',callback_data='export_statistic_finance')
    in9 = InlineKeyboardButton(text='⬅️ Назад', callback_data='management_users_admin_')
    markup_export_data.add(in1)
    markup_export_data.add(in2)
    markup_export_data.add(in3)
    markup_export_data.add(in4)
    markup_export_data.add(in5)
    markup_export_data.add(in6)
    markup_export_data.add(in7)
    markup_export_data.add(in8)
    markup_export_data.add(in9)
    return markup_export_data

def back_excel_data():
    markup_back_excel = InlineKeyboardMarkup()
    markup_back_excel.row(InlineKeyboardButton(text='⬅️ Назад', callback_data='management_users_admin_'))
    return markup_back_excel

def cancel_edit_all_users_procent():
    markup_cancel_edit = InlineKeyboardMarkup()
    markup_cancel_edit.row(InlineKeyboardButton(text='Отмена 🚫', callback_data='cancel_edit_procent_all_users'))
    return markup_cancel_edit

def give_list_admins(_admins):
    markup_list_admin = InlineKeyboardMarkup()
    for i in _admins:
        in1 = InlineKeyboardButton(text=f'{i[2]}', callback_data=f'give_admin_id_{i[1]}')
        markup_list_admin.add(in1)
    in2 = InlineKeyboardButton(text='⬅️ Назад', callback_data='admin_')
    markup_list_admin.add(in2)
    return markup_list_admin

def edit_admins(_id_admin):
    markup_edit_admins = InlineKeyboardMarkup()
    in1 = InlineKeyboardButton(text='Удалить из Админов ⛔️', callback_data=f'del_admin_id_{_id_admin}')
    in2 = InlineKeyboardButton(text='Сообщение 💬', callback_data=f'push_msg_admin_id_{_id_admin}')
    in3 = InlineKeyboardButton(text='Изменить Баланс ✏️', callback_data=f'edit_balance_admin_id_{_id_admin}')
    in4 = InlineKeyboardButton(text='Изменить Процент ✏️', callback_data=f'edit_procent_admin_id_{_id_admin}')
    in5 = InlineKeyboardButton(text='⬅️ Назад', callback_data=f'management_admins_admin_')
    markup_edit_admins.add(in1, in2)
    markup_edit_admins.add(in3, in4)
    markup_edit_admins.add(in5)
    return markup_edit_admins

def back_in_edit_admins():
    markup_back_admins = InlineKeyboardMarkup()
    markup_back_admins.row(InlineKeyboardButton(text='⬅️ Назад', callback_data='management_admins_admin_'))
    return markup_back_admins

def cancel_in_edit_admins(method):
    markup_back_admins = InlineKeyboardMarkup()
    markup_back_admins.row(InlineKeyboardButton(text='Отмена 🚫', callback_data=f'cancel_edit_admins_{method}'))
    return markup_back_admins

def captcha_users(method, id_ref):
    markup_captcha = InlineKeyboardMarkup(row_width=6)

    for i in range(1, 6):
        markup_captcha.row(InlineKeyboardButton(text=f'{i}', callback_data=f'captcha_number_{i}_{method}_{id_ref}'))

    return markup_captcha

def update_photo_captcha_users():
    markup_photo_captcha = InlineKeyboardMarkup()
    markup_photo_captcha.row(InlineKeyboardButton(text='Обновить 🔄', callback_data='update_catpcha'))
    return markup_photo_captcha

def select_method_captcha_bot():
    markup_select_captcha = InlineKeyboardMarkup()
    in1 = InlineKeyboardButton(text='Выбор Цифры 🔢', callback_data='add_captcha_1')
    in2 = InlineKeyboardButton(text='Ввод Цифр с Изоб. 🖼', callback_data='add_captcha_2')
    in3 = InlineKeyboardButton(text='Решение Уровнений 🧮', callback_data='add_captcha_3')
    in4 = InlineKeyboardButton(text='Отключить капчу 🟠', callback_data='add_captcha_0')
    in5 = InlineKeyboardButton(text='⬅️ Назад', callback_data='management_bot_admin_')
    markup_select_captcha.add(in1, in2)
    markup_select_captcha.add(in3)
    markup_select_captcha.add(in4)
    markup_select_captcha.add(in5)
    return markup_select_captcha


def select_edit_type_ref_system():
    markup_edit_ref_system = InlineKeyboardMarkup()
    markup_edit_ref_system.row(InlineKeyboardButton(text='💸 Вознаграждение RUB', callback_data='manager_bot_edit_8'),
                            InlineKeyboardButton(text='⚖️ Вознаграждение Процент', callback_data='manager_bot_edit_9'))
    markup_edit_ref_system.row(InlineKeyboardButton(text='⬅️ Назад', callback_data='management_bot_admin_'))
    return markup_edit_ref_system


def reply_message_in_support(_id_user):
    markup_reply_message_admin = InlineKeyboardMarkup()
    in1 = InlineKeyboardButton(text='Спросить 💬', callback_data=f'admin_to_ask_{_id_user}')
    in2 = InlineKeyboardButton(text='Известить ❕', callback_data=f'admin_notify_{_id_user}')
    in3 = InlineKeyboardButton(text='Бан 💢', callback_data=f'set_ban_{_id_user}')
    markup_reply_message_admin.add(in1, in2, in3)
    return markup_reply_message_admin


def reply_message_user_in_support(_id_admin):
    markup_reply_message_user = InlineKeyboardMarkup()
    in1 = InlineKeyboardButton(text='Ответить 💬', callback_data=f'users_to_ask_{_id_admin}')
    in2 = InlineKeyboardButton(text='Благодарить 🙏', callback_data=f'users_thank_{_id_admin}')
    in3 = InlineKeyboardButton(text='Закрыть ❌', callback_data=f'reply_message_user_in_support_close_id_{_id_admin}')
    markup_reply_message_user.add(in1, in2)
    markup_reply_message_user.add(in3)
    return markup_reply_message_user


def confirm_the_ban_all_users():
    markup_success_ban = InlineKeyboardMarkup()
    markup_success_ban.row(InlineKeyboardButton(text='Заблокировать 💢', callback_data='confirm_all_ban_users'),
                           InlineKeyboardButton(text='⬅️ Назад', callback_data='management_users_admin_'))
    return markup_success_ban

def confirm_the_unban_all_users():
    markup_success_ban = InlineKeyboardMarkup()
    markup_success_ban.row(InlineKeyboardButton(text='Разблокировать ✅', callback_data='confirm_all_unban_users'),
                           InlineKeyboardButton(text='⬅️ Назад', callback_data='management_users_admin_'))
    return markup_success_ban

def cancel_reply_message_for_users():
    markup_cancel_reply_message = InlineKeyboardMarkup()
    markup_cancel_reply_message.row(InlineKeyboardButton(text='Отмена 🚫', callback_data='cancel_reply_message'))
    return markup_cancel_reply_message