from aiogram import types
import aiogram
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.storage import FSMContext

from loader import dp, bot
from keyboards import inline_keyboards as ikb
from data.db import DB
from states.state import TopUpBalance
from libs import config

@dp.callback_query_handler(text='top_up_balance_')
async def call_top_up_balance(call: types.CallbackQuery):
    with DB() as db:
        get_ban_list = db.give_is_ban_users(call.message.chat.id)
        if get_ban_list:
            get_info_ban = db.give_ban_info_user(call.message.chat.id)
            await call.message.edit_text(f'<b>Вы были заблокированы!\n\nПричина:</b> <i>{get_info_ban[1]}</i>')
            return

    await call.message.edit_text('Выберите способ пополнения', reply_markup=ikb.select_top_up_balance())

@dp.callback_query_handler(Text('choise_method_all_'))
async def call_choise_method_all(call: types.CallbackQuery):
    await call.message.edit_text('<b>Выберите способ пополнения</b>', reply_markup=ikb.select_top_up_balance())

@dp.callback_query_handler(Text(startswith='paymaster_'))
async def call_paymaster(call: types.CallbackQuery, state: FSMContext):
    await state.set_state(TopUpBalance.max_summ)
    msg_top_up = 'Пришлите сумму пополнения в RUB\n'
    with DB() as db:
        get_max_and_min_summ = db.give_max_and_min_summ()

    async with state.proxy() as data:
        data['max_summ'] = int(get_max_and_min_summ[0])
        data['min_summ'] = int(get_max_and_min_summ[1])

    if int(get_max_and_min_summ[0]) != 0:
        msg_top_up += f'Макс.cумма: {get_max_and_min_summ[0]} RUB\n'

    if int(get_max_and_min_summ[1]) != 0:
        msg_top_up += f'Мин.cумма: {get_max_and_min_summ[1]} RUB'

    await call.message.edit_text(msg_top_up, reply_markup=ikb.cancel_top_up_balance())

@dp.message_handler(state=TopUpBalance.max_summ)
async def top_up_balance_get_state(message: types.Message, state: FSMContext):
    try:
        user_summ = int(message.text)

    except ValueError:
        await message.answer('Введите число!\n'
                             '<b>[?] Без плавающей точки</b>', reply_markup=ikb.cancel_top_up_balance())
        try:
            await bot.delete_message(message.chat.id, message_id=message.message_id-1)
        except aiogram.utils.exceptions.MessageToDeleteNotFound:
            pass
        return        
    
    async with state.proxy() as data:
        _max_summ = data['max_summ']
        _min_summ = data['min_summ']

    if _max_summ != 0:
        if user_summ > _max_summ:
            await message.answer(f'Максимальная сумма <code>{_max_summ}</code> RUB!', reply_markup=ikb.cancel_top_up_balance())
            return

    if _min_summ != 0:
        if user_summ < _min_summ:
            await message.answer(f'Минимальная сумма <code>{_min_summ}</code> RUB!', reply_markup=ikb.cancel_top_up_balance())
            return

    if _max_summ == 0 or _min_summ == 0:
        if user_summ > 1_000_000:
            await message.answer(f'Максимальная сумма <code>1000000</code> RUB!', reply_markup=ikb.cancel_top_up_balance())
            return

        if user_summ < 10:
            await message.answer(f'Минимальная сумма <code>10</code> RUB!', reply_markup=ikb.cancel_top_up_balance())
            return
        
    PRICE = types.LabeledPrice(label=config.label_top_up, amount=user_summ * 100) # в копейках
    await bot.send_invoice(message.chat.id,
                            title=config.title_top_up,
                            description=config.description_top_up,
                            provider_token=config.PAYMENTS_TOKEN,
                            currency='rub',
                            is_flexible=False,
                            prices=[PRICE],
                            start_parameter='one-month-subsciption',
                            payload='test-invoice-payload')
    
    await message.answer('<b>Вам отправлен Чек на оплату</b>', reply_markup=ikb.back_in_main_menu())
    await state.finish()