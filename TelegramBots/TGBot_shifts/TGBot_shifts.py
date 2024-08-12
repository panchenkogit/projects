import telebot
from telebot import types
import sqlite3
import os
from datetime import datetime


API_TOKEN = ''
bot = telebot.TeleBot(API_TOKEN)

# Функция для создания базы данных
def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS shifts (
            shift_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            user_name TEXT,
            start_time TEXT,
            end_time TEXT,
            FOREIGN KEY(user_id) REFERENCES users(user_id)
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

# Функция для получения открытых смен
def get_open_shifts():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('SELECT shift_id, user_name, start_time FROM shifts WHERE end_time IS NULL')
    shifts = c.fetchall()
    conn.close()
    return shifts

# Функция для получения всех смен
def get_all_shifts():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('SELECT user_name, start_time, end_time FROM shifts')
    shifts = c.fetchall()
    conn.close()
    return shifts


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

# Обработчик кнопки "Открыть смену"
@bot.message_handler(func=lambda message: message.text == "Открыть смену")
def open_shift(message):
    users = get_users()
    if not users:
        bot.send_message(message.chat.id, "Нет пользователей для выбора.")
        start_message(message)
        return

    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    for _, name in users:
        btn = types.KeyboardButton(name)
        markup.add(btn)
    btn_back = types.KeyboardButton("Назад")
    markup.add(btn_back)

    bot.send_message(message.chat.id, "Выберите пользователя для открытия смены:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text in [user[1] for user in get_users()])
def start_shift(message):
    user_name = message.text
    user_id = next(user[0] for user in get_users() if user[1] == user_name)

    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute('INSERT INTO shifts (user_id, user_name, start_time) VALUES (?, ?, ?)', (user_id, user_name, start_time))
    conn.commit()
    conn.close()

    bot.send_message(message.chat.id, f"Смена для пользователя {user_name} открыта.")
    start_message(message)

# Обработчик кнопки "Завершить смену"
@bot.message_handler(func=lambda message: message.text == "Завершить смену")
def close_shift(message):
    open_shifts = get_open_shifts()
    if not open_shifts:
        bot.send_message(message.chat.id, "Нет открытых смен для закрытия.")
        start_message(message)
        return

    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    for shift_id, user_name, start_time in open_shifts:
        btn = types.KeyboardButton(f"{user_name} ({start_time})")
        markup.add(btn)
    btn_back = types.KeyboardButton("Назад")
    markup.add(btn_back)

    bot.send_message(message.chat.id, "Выберите смену для закрытия:", reply_markup=markup)

@bot.message_handler(func=lambda message: any(shift[1] in message.text for shift in get_open_shifts()))
def end_shift(message):
    user_name = message.text.split(' ')[0]
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute('UPDATE shifts SET end_time = ? WHERE user_name = ? AND end_time IS NULL', (end_time, user_name))
    conn.commit()
    conn.close()

    bot.send_message(message.chat.id, f"Смена для пользователя {user_name} закрыта.")
    start_message(message)

# Обработчик кнопки "Все смены"
@bot.message_handler(func=lambda message: message.text == "Все смены")
def show_all_shifts(message):
    all_shifts = get_all_shifts()
    if not all_shifts:
        bot.send_message(message.chat.id, "Нет смен для отображения.")
        start_message(message)
        return

    shifts_text = "\n".join(f"Пользователь: {user_name}, Открыта: {start_time}, Закрыта: {end_time or 'Открыта'}"
                            for user_name, start_time, end_time in all_shifts)
    bot.send_message(message.chat.id, f"Все смены:\n{shifts_text}")
    start_message(message)

# Обработчик кнопки "Назад"
@bot.message_handler(func=lambda message: message.text == "Назад")
def back_to_main_menu(message):
    start_message(message)

# Инициализация базы данных и таблицы
init_db()

# Запуск бота
bot.polling(none_stop=True)

