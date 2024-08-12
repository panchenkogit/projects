from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram import F, Router
import keyboards as kb
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

router = Router()

class Reg(StatesGroup):
    name = State()
    number = State()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer("Привет!", reply_markup=kb.main)

@router.message(Command("links"))
async def get_link_tg(message: Message):
    await message.answer("Ссылки для связи со мной:", reply_markup=kb.links)

@router.message(Command("get_cars"))
async def get_cars(message: Message):
    await message.answer("Список всех машин:", reply_markup=await kb.inline_cars())

@router.callback_query(F.data == "link_to_tg")
async def link_to_tg(callback: CallbackQuery):
    await callback.answer("")
    await callback.message.answer("Привет!Снова.")

@router.callback_query(F.data == "cars")
async def view_cars(callback: CallbackQuery):
    await callback.answer("Каталог машин")
    await callback.message.edit_text('Вот все машины:', reply_markup=await kb.inline_cars())

@router.message(Command('reg'))
async def get_user_name(message: Message, state: FSMContext):
    await state.set_state(Reg.name)
    await message.answer("Введите ваше имя")

@router.message(Reg.name)
async def get_user_number(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Reg.number)
    await message.answer("Введите номер телефона")
 
@router.message(Reg.number)
async def two_tree(message: Message, state: FSMContext):
    await state.update_data(number=message.text)
    data = await state.get_data()
    await message.answer(f"Спасибо,регистрация завершнеа!\nПроверьте данные.\nИмя: {data['name']} Номер: {data["number"]}")
    await state.clear()