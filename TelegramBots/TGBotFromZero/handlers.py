from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram import F, Router

import asyncio

import random

from config import ADMIN_ID

import database.requests as rq

import keyboard as kb

import dictionary as dict


router = Router()
word = ''

@router.message(CommandStart())
async def cmd_start(message: Message): 
    await rq.add_user(message.from_user.id, message.from_user.username)
    if message.from_user.id == ADMIN_ID:
        await message.answer(f"Добро пожаловать, администратор {message.from_user.username}", reply_markup=kb.admin_keyboard)
    else:
        await message.answer("Привет!Я бот для обучения английскому языку.Нажми на кнопку,когда будешь готов.\nПодробнее о формате обучения можете узнать,написав команду /help", reply_markup=kb.main)

@router.message(Command('help'))
async def get_help(message: Message):
    await message.answer("Прицпин простой.Вам присылают слово на английском языке.Ваша задача-перевести его и написать в чат ответ.Если он верный,то вам будет отправлено следующее слово.Если нет,у вас будет бесконечное число попыток дял ввода верного варианта ответа.")


@router.callback_query(F.data == 'start_learning')
async def start_learning(callback: CallbackQuery):
    await callback.answer("Вы начали обучение")
    await get_word(callback.message)
    
@router.callback_query(F.data == 'set')
async def set(callback: CallbackQuery):
    await callback.answer('Вы выбрали Настройки')
    await callback.message.answer("Какое действие вы хотите выполнить?", reply_markup=kb.set_keyboard)

@router.callback_query(F.data == 'view_all_user')
async def view_all_user(callback: CallbackQuery):
    all_user = await rq.view_all_user()
    all_user_keyboard = await kb.all_user(all_user)
    await callback.answer("")
    await callback.message.answer("Вот список пользователей", reply_markup=all_user_keyboard.as_markup())

@router.callback_query()
async def handle_callback(callback: CallbackQuery):
    # Логируем все callback_data
    print(f"Callback data: {callback.data}")

@router.callback_query(F.data == "user_{user.tg_id}")
async def user_action(callback: CallbackQuery):
    id_user = callback.data()
    await callback.answer(f"Вы выбрали пользователя {id_user}")  
    await callback.message.answer("Действия с пользователем", reply_markup=await kb.user_action)


@router.message(Command('word'))
async def get_word(message: Message):
    global word
    word = random.choice(list(dict.word_dict.keys()))
    await message.answer(f"Переведите слово {word}")

@router.message()
async def check_translate(message: Message):
    answer = message.text.strip().lower()
    right = dict.word_dict[word]
    if answer == right:
        await message.answer(f"Верно! {word} переводится как {right}")
        await asyncio.sleep(5)
        await get_word(message)
    else:
         await message.answer("Неверно! Попробуй ещё раз или введи /word, чтобы пропустить это слово.")


        


    

        
