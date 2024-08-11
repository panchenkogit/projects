from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
import asyncio
import datetime
from bot import dp

@dp.message(Command('start'))
async def com_start(message: types.Message):
    await get_datetime(message)
    await message.answer(f"Привет, {message.chat.username}.\nКоторый час у тебя сейчас?")   

async def get_datetime(message: types.Message):
    forward_date = message.date
    formatted_time = forward_date.strftime("%H:%M")
    #user_id = message."Помоги тут написать"
    user_name = message.chat.username
