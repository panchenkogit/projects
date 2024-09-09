from aiogram import Dispatcher, Bot

import asyncio

import logging


from config import TOKEN

from handlers import router
from database.models import async_main

logging.basicConfig(level=logging.INFO)

async def main():
    await async_main()
    bot = Bot(TOKEN)
    dp = Dispatcher()  
    dp.include_router(router)
    await dp.start_polling(bot)
    

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот выключен.")
