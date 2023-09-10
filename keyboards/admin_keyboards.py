from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def main_admin_panel():
    main_panel = InlineKeyboardMarkup()
    in1 = InlineKeyboardButton(text='Добавить Каталог ❇️', callback_data='add_catalogs_admin_')
    in2 = InlineKeyboardButton(text='Добавить Товар ❇️', callback_data='add_products_admin_')

    in3 = InlineKeyboardButton(text='Удалить Каталог ❌', callback_data='delete_catalogs_admin_')
    in4 = InlineKeyboardButton(text='Удалить Товар ❌', callback_data='delete_products_admin_')

    in5 = InlineKeyboardButton(text='Изменить Товар ✏️', callback_data='edit_old_product_admin_')

    in6 = InlineKeyboardButton(text='Рассылка 📬', callback_data='spam_users_admin_')
    in7 = InlineKeyboardButton(text='Статистика 📊', callback_data='statistic_admin_')

    in8 = InlineKeyboardButton(text='Бот 🤖', callback_data='management_bot_admin_')
    in9 = InlineKeyboardButton(text='Пользователи 👥', callback_data='management_users_admin_')
    in10 = InlineKeyboardButton(text='Сообщения 💬', callback_data='message_for_admin_')
    in11 = InlineKeyboardButton(text='Админы 🛂', callback_data='management_admins_admin_')

    in12 = InlineKeyboardButton(text='Закрыть Админку 🔐', callback_data='close_admin_panel_')

    main_panel.add(in1, in2)
    main_panel.add(in3, in4)
    main_panel.add(in5)
    main_panel.add(in6, in7)
    main_panel.add(in8, in9)
    main_panel.add(in10, in11)
    main_panel.add(in12)


    return main_panel
