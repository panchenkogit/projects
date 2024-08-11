from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
import asyncio
import datetime
from config import TOKEN

bot = Bot(TOKEN)
dp = Dispatcher()

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())