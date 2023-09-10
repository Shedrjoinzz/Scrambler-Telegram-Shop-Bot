
import sys
import os
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from data.db import DB

BOT_TOKEN = "6686331573:AAE4_g9iHqV_odXsWh5OSOLnYjVsOSt5m-E"
PAYMENTS_TOKEN = "1744374395:TEST:ac85ef24a9f4b47fb5c1" # до этого был тестовый токен
USERNAME_BOT = "@ScramblerShopBot" # можно и с "@" или без "@" разницы нет

# EN You can write your text here
# RU Вы можете написать свой текст здесь


# //////////////////////////
title_top_up = 'Магазин Бот'
label_top_up = 'Пополнение баланса Магазина'
description_top_up = 'Пополнение Магазин Бота через PayMaster безопасно, быстро, надёжно!'
# //////////////////////////


def id_admin():

    with DB() as db:
        get_list_admins =  db.give_all_admin_list()
    
    list = [1234567]  # EN Insert your 1234567 id here, to add subsequent administrators, open the admin panel and Administration Controls.
                         # list index 0 main admin
                         # RU Введите здесь свой идентификатор 1234567, чтобы добавить последующих администраторов, откройте панель администратора и элементы управления администрированием.
                         # индекс списка 0 главный администратор
                         
    for i in get_list_admins:
        list.append(i[1])

    return list