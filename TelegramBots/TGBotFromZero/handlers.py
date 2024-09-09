from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram import F, Router

import random

import database.requests as rq

import keyboard as kb

import dictionary as dict

router = Router()

word = ''

@router.message(CommandStart())
async def cmd_start(message: Message):
    await rq.add_user(message.from_user.id, message.from_user.username)
    await message.answer("Привет!Я бот для обучения английскому языку.Нажми на кнопку,когда будешь готов.\nПодробнее о формате обучения можете узнать,написав команду /help", reply_markup=kb.main)

@router.message(Command('help'))
async def get_help(message: Message):
    await message.answer("Прицпин простой.Вам присылают слово на английском языке.Ваша задача-перевести его и написать в чат ответ.Если он верный,то вам будет отправлено следующее слово.Если нет,у вас будет бесконечное число попыток дял ввода верного варианта ответа.")


@router.callback_query(F.data == 'start_learning')
async def start_learning(callback: CallbackQuery):
    await callback.answer("Вы начали обучение.")
    await get_word(callback.message)
    

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
        await get_word(message)
    else:
         await message.answer("Неверно! Попробуй ещё раз или введи /word, чтобы пропустить это слово.")


        


    

        
