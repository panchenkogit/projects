from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

main = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Ссылка на ТГ",callback_data="link_to_tg")],
    [InlineKeyboardButton(text="Машины", callback_data="cars")]
], 
resize_keyboard=True,
input_field_placeholder="Выберите пункт меню")


links = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='VK', url="https://vk.com/id495133000")],
    [InlineKeyboardButton(text='TG', url="https://t.me/jfkspapzkKzjj")]
])

cars = ['Tesla', 'Mersedes','Lada']

async def inline_cars():
    keyboard = InlineKeyboardBuilder()
    for car in cars:
        keyboard.add(InlineKeyboardButton(text=car, callback_data="cars"))
    return keyboard.adjust(2).as_markup()

