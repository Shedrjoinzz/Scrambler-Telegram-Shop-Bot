from aiogram.dispatcher.filters.state import State, StatesGroup

class CountBasketProduct(StatesGroup):
    id_product = State()
    max_count = State()
    count_product = State()

class CountAddBasketProduct(StatesGroup):
    id_product = State()
    max_count = State()
    count_product = State()

class AddCatalogs(StatesGroup):
    old_name_catalog = State()
    name_catalog = State()

class AddProducts(StatesGroup):
    id_catalog = State()
    product = State()

class AdvancedAddProducts(StatesGroup):
    id_catalog = State()
    name_product = State()
    description_product = State()
    price_product = State()
    count_product = State()
    link_product = State()
    success = State()

class SpamUsers(StatesGroup):
    _message = State()
    _save_message = State()

class TopUpBalance(StatesGroup):
    max_summ = State()
    min_summ = State()

class SetCharacteristic(StatesGroup):
    id_call_msg = State()

class EditProductOne(StatesGroup):
    id_product = State()
    id_call_msg = State()

class MessengerAdmin(StatesGroup):
    id_user = State()
    message_user = State()

class MessengerUser(StatesGroup):
    id = State()
    message_admin = State()
    method = State()

class Support(StatesGroup):
    id_user = State()
    text = State()

class EditOldProduct(StatesGroup):
    id_product = State()

class EditUserInfo(StatesGroup):
    id_user = State()
    summ_balance = State()
    procent = State()
    info_ban_user = State()
    push_msg_user = State()

class EditProcentAllUsers(StatesGroup):
    procent = State()

class PushAdminMessage(StatesGroup):
    id_admin = State()
    admin_push_message = State()

class EditAdminBalance(StatesGroup):
    id_admin = State()
    admin_balance_rub = State()

class EditAdminProcent(StatesGroup):
    id_admin = State()
    admin_procent = State()

class AntiUsersBotSecurityNumbers(StatesGroup):
    number = State()

class AntiUsersBotSecurityPhotoNumbers(StatesGroup):
    photo_number = State()
    id_ref = State() 

class AntiUsersBotSecuritySolvingEquations(StatesGroup):
    answer = State()
    id_ref = State()

class ToAskAdmin(StatesGroup):
    id_user = State()

class NotifyAdmin(StatesGroup):
    id_user = State()

class ToAskUsers(StatesGroup):
    id_admin = State()

class SetInfoBanUsers(StatesGroup):
    id_user = State()
    info_ban_user = State()
