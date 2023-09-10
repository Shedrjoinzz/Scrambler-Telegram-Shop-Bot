from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from libs import config as cfg


##=> ИНИЦИАЛИЗАЦИЯ БОТА
##########################################################
bot = Bot(token=cfg.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
print('Сервер запущен')
