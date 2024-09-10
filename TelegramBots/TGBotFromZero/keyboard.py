from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

main = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Начать обучение", callback_data="start_learning")]
])

admin_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Начать обучение", callback_data="start_learning"),
    InlineKeyboardButton(text="Настройки", callback_data="set")]
])

set_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Посмотреть всех пользователей", callback_data="view_all_user")],
    [InlineKeyboardButton(text="Добавить новое слово", callback_data="add_char")],
    [InlineKeyboardButton(text="Изменить таймер", callback_data="change_timer")],
    [InlineKeyboardButton(text="Назад", callback_data="go_back")]
])

user_action = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Удалить пользователя", callback_data="delete_user"),
    InlineKeyboardButton(text="Добавить пользователя", callback_data="delete_user")],
    [InlineKeyboardButton(text="Назад", callback_data="go_back")]
])

async def all_user(all_user):
    all_user_keyboard = InlineKeyboardBuilder()
    for user in all_user:
        all_user_keyboard.add(InlineKeyboardButton(text=user.username, callback_data=f"user_{user.tg_id}"))
    all_user_keyboard.add(InlineKeyboardButton(text="Назад", callback_data="go_back"))
    return all_user_keyboard.adjust(1)