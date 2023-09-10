from aiogram import executor
import aiogram
import logging

from loader import dp
from libs.config import *
from libs.set_bot_commands import set_default_commands
from handlers import *
from handlers.headers.anti_flood import ThrottlingMiddleware

logging.basicConfig(level=logging.INFO)

async def on_startup(dispatcher):
    await set_default_commands(dispatcher)

if __name__ == "__main__":
    try:
        print('Бот запущен')
        dp.middleware.setup(ThrottlingMiddleware())
        executor.start_polling(dp, on_startup=on_startup, skip_updates=False)
    except aiogram.utils.exceptions.NetworkError:
        print('ОЩИБКА: Не удается подключиться к хосту, проверьте подключение к интернету')
    except aiogram.utils.exceptions.ValidationError:
        print('Токен недействителен!\nУкажите ТОКЕН!')