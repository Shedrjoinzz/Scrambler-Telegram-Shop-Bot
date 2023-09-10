from aiogram.types.message import ContentType
from aiogram import types

from loader import dp, bot
from handlers import commands as com
from keyboards import inline_keyboards as ikb
from data.db import DB


@dp.pre_checkout_query_handler(lambda query: True)
async def pre_check_query(pre_checkout_q: types.PreCheckoutQuery):
      await bot.answer_pre_checkout_query(pre_checkout_q.id, ok=True)


@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
async def buy_product_handler(message: types.Message):
      await com.delete_all_message_chat(message)
      get_top_up_summ = int(message.successful_payment.total_amount) // 100

      _message = f'Ваш баланс пополнен на <b>{get_top_up_summ} {message.successful_payment.currency}</b> успешно!\n'
      
      with DB() as db:
            get_procent = db.give_info_user('procent', message.chat.id)
            
            _top_up_summ_in_procent = get_top_up_summ * get_procent[0] // 100

            if get_procent[0] != 0:
                  _message += f'<b>Вы получили {get_procent[0]}% (+{_top_up_summ_in_procent} RUB) от пополнения!</b>'
                  db.update_procent_users(0, message.chat.id)

            db.give_top_up_balance_rub(message.chat.id, message.successful_payment.total_amount // 100 + int(_top_up_summ_in_procent))
            db.add_top_up_money_in_finance(int(message.successful_payment.total_amount) // 100)
            
      await message.answer(f'{_message}',
                           reply_markup=ikb.back_basket_list('back_menu'))