from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram import F, Router
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

import asyncio
import random

from config import ADMIN_ID
import database.requests as rq
import keyboard as kb
import dictionary as dict


router = Router()

class Word(StatesGroup):
    give_word = State()
    get_translate = State()

@router.message(~F.text & ~F.text.startswith('/'))
async def handle_non_text(message: Message):
    await message.answer("Это сообщение не является текстом или командой. Что вы хотели отправить?")

@router.message(CommandStart())
async def cmd_start(message: Message):
    user_id = message.from_user.id
    username = message.from_user.username
    if username is None:
        username = "user" 

    try:
        user_bot = await rq.add_user(user_id, username)
    except Exception as e:
        await message.answer("Произошла ошибка при добавлении пользователя. Попробуйте еще раз.")
        return
    
    if message.from_user.id == ADMIN_ID:
        await message.answer(f"Добро пожаловать, администратор {username}", reply_markup=kb.admin_keyboard)
    elif not user_bot:
        await message.answer(f"Привет, {username}", reply_markup=kb.main)
    else:
        await message.answer("Привет! Я бот для обучения английскому языку. Нажми на кнопку, когда будешь готов.\nПодробнее о формате обучения можете узнать, написав команду /help", reply_markup=kb.main)

@router.message(Command('help'))
async def get_help(message: Message):
    await message.answer("Прицпин простой.Вам присылают слово на английском языке.Ваша задача-перевести его и написать в чат ответ.Если он верный,то вам будет отправлено следующее слово.Если нет,у вас будет бесконечное число попыток дял ввода верного варианта ответа.")

@router.callback_query(F.data == 'start_learning')
async def start_learning(callback: CallbackQuery, state: FSMContext):
    await callback.answer("Вы начали обучение")
    await get_word(callback.message, state)
    
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

@router.callback_query(F.data.startswith("delete_"))
async def delete_user(callback: CallbackQuery):
    tg_id = callback.data.split('_')[1]
    res_del = await rq.delete_user(tg_id)
    if res_del == False:
        await callback.message.answer("Пользователь не найден")
    else:
        await callback.answer()
        await callback.message.answer("Пользователь успешно удалён")

@router.callback_query(F.data.startswith("user_"))
async def user_action(callback: CallbackQuery):
    tg_id = callback.data.split('_')[1]
    user = await rq.get_user_by_id(tg_id)
    await callback.answer(f"Вы выбрали пользователя {user.username}")  
    await callback.message.answer(f"Действия с пользователем {user.username}", reply_markup=await kb.user_action_keyboard(tg_id))

@router.message(Command('word'))
async def get_word(message: Message, state: FSMContext):
        word = random.choice(list(dict.word_dict.keys()))
        await state.update_data(give_word=word)
        await message.answer(f"Переведите слово {word}")
        await state.set_state(Word.get_translate)

@router.message(Word.get_translate)
async def check_translate(message: Message, state: FSMContext):
    await state.update_data(get_translate=message.text)
    data = await state.get_data()
    right = dict.word_dict[data['give_word']].lower()
    if data['get_translate'].lower() == right:
        await message.answer(f"Верно! {data['give_word']} переводится как {right}")
        await asyncio.sleep(5)
        await get_word(message, state)
    else:
         await message.answer("Неверно! Попробуй ещё раз или введи /word, чтобы пропустить это слово.")

