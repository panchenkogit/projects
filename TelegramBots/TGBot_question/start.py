from aiogram import Bot, Dispatcher

from app.config import TOKEN
from app.handlers import router
from database.models import async_main

import asyncio

import logging

logging.basicConfig(level="INFO")

async def main():
    dp = Dispatcher()
    bot = Bot(token=TOKEN)
    dp.include_router(router)
    await async_main()
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Конец")