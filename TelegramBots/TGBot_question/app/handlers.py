from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandStart
from aiogram import Router, F
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

import requests

from app.config import BOT_NAME
import app.keyboard as kb

import database.requests as rq

router = Router()

class Register(StatesGroup):
    name = State()
    chanell_link = State()

# Хендлер для команды /start
@router.message(CommandStart())
async def com_start(message: Message):
    user_id = message.from_user.id

    # Проверяем, есть ли в команде /start переданный параметр (ID другого пользователя)
    if message.text.startswith('/start ') and len(message.text.split()) > 1:
        target_user_id = message.text.split()[1]

        # Сохраняем связь между пользователями
        await rq.save_target_user_id(user_id, target_user_id)

        await message.answer("Вы перешли по уникальной ссылке! Напишите ваш вопрос и пользователь получит его.")
    else:
        result = await rq.add_new_user(user_id)
        if not result:
            await message.answer("Бот активирован. Чтобы зарегистрироваться, напишите команду /reg")
        else:
            await message.answer("Добро пожаловать!")

# Хендлер для регистрации пользователя
@router.message(Command('reg'))
async def cmd_reg(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(Register.name)
    await message.answer("Пожалуйста, введите ваше имя")

# Получение имени
@router.message(F.text, Register.name)
async def get_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Register.chanell_link)
    await message.answer("Введите вашу ссылку на свой телеграм канал")

# Получение ссылки на канал
@router.message(Register.chanell_link)
async def get_link(message: Message, state: FSMContext):
    await state.update_data(chanell_link=message.text)
    data = await state.get_data()
    name = data['name']
    chanell_link = data['chanell_link']
    user_id = message.from_user.id
    await message.answer(f"Ваши данные:\nИмя - {name}\nСсылка - {chanell_link}")
    await rq.update_user_data(name, chanell_link, user_id)
    await state.clear()
    
    unique_link = f"https://t.me/{BOT_NAME}?start={message.from_user.id}"
    await message.reply(f"Вот твоя уникальная ссылка для получения вопросов: {unique_link}")


@router.message(F.text)
async def handle_question(message: Message):
    user_id = message.from_user.id
    target_user_id = await rq.get_target_user_id(user_id)

    if target_user_id:  
        question = message.text
        await message.bot.send_message(target_user_id, f"Вам задали вопрос: {question}")
        await message.answer("Ваш вопрос отправлен!")
    else:
        await message.answer("Вы не связаны с другим пользователем для отправки вопроса.")
