import telebot
from telebot import types
import sqlite3
import os

# Ваш реальный токен
API_TOKEN = '7385731370:AAG-Nh5QFHTO1WLHR1k8Q5T1MNZe12cvTtk'
bot = telebot.TeleBot(API_TOKEN)

# Функция для создания базы данных и таблицы, если их нет
def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Функция для получения списка пользователей из базы данных
def get_users():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('SELECT user_id, name FROM users')
    users = c.fetchall()
    conn.close()
    return users

# Функция для создания клавиатуры с кнопками меньшего размера
def create_small_keyboard(buttons):
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    for button in buttons:
        markup.add(types.KeyboardButton(button))
    return markup

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start_message(message):
    markup = create_small_keyboard(["Смены", "Пользователи"])
    bot.send_message(message.chat.id, "Привет! Выберите действие:", reply_markup=markup)

# Обработчик кнопки "Смены"
@bot.message_handler(func=lambda message: message.text == "Смены")
def show_shift_buttons(message):
    markup = create_small_keyboard(["Открыть смену", "Завершить смену", "Все смены"])
    bot.send_message(message.chat.id, "Выберите действие со сменой:", reply_markup=markup)

# Обработчик кнопки "Пользователи"
@bot.message_handler(func=lambda message: message.text == "Пользователи")
def show_user_buttons(message):
    markup = create_small_keyboard(["Добавить пользователя", "Удалить пользователя"])
    bot.send_message(message.chat.id, "Выберите действие с пользователями:", reply_markup=markup)

# Обработчик кнопки "Добавить пользователя"
@bot.message_handler(func=lambda message: message.text == "Добавить пользователя")
def add_user(message):
    msg = bot.send_message(message.chat.id, "Введите ID пользователя:")
    bot.register_next_step_handler(msg, process_user_id)

def process_user_id(message):
    try:
        user_id = int(message.text)
        msg = bot.send_message(message.chat.id, "Введите имя пользователя:")
        bot.register_next_step_handler(msg, process_user_name, user_id)
    except ValueError:
        msg = bot.send_message(message.chat.id, "Некорректный ID. Пожалуйста, введите число.")
        bot.register_next_step_handler(msg, process_user_id)

def process_user_name(message, user_id):
    name = message.text
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('INSERT OR REPLACE INTO users (user_id, name) VALUES (?, ?)', (user_id, name))
    conn.commit()
    conn.close()
    bot.send_message(message.chat.id, f"Пользователь {name} добавлен.")
    start_message(message)  # Возвращаем в главное меню

# Обработчик кнопки "Удалить пользователя"
@bot.message_handler(func=lambda message: message.text == "Удалить пользователя")
def delete_user(message):
    users = get_users()
    if not users:
        bot.send_message(message.chat.id, "Нет пользователей для удаления.")
        start_message(message)  # Возвращаем в главное меню
        return
    
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    for _, name in users:
        btn = types.KeyboardButton(name)
        markup.add(btn)
    btn_back = types.KeyboardButton("Назад")
    markup.add(btn_back)
    
    bot.send_message(message.chat.id, "Выберите пользователя для удаления:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text in [user[1] for user in get_users()])
def confirm_user_deletion(message):
    name = message.text
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('DELETE FROM users WHERE name = ?', (name,))
    conn.commit()
    conn.close()
    bot.send_message(message.chat.id, f"Пользователь {name} удален.")
    start_message(message)  # Возвращаем в главное меню

# Обработчик кнопки "Назад"
@bot.message_handler(func=lambda message: message.text == "Назад")
def back_to_main_menu(message):
    start_message(message)  # Возвращаем в главное меню

# Инициализация базы данных и таблицы
init_db()

# Запуск бота
bot.polling(none_stop=True)
