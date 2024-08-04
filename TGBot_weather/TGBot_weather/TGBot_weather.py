from config import TOKEN, API_WHEATHER_TOKEN,weather_descriptions
import telebot
from telebot import types
import json
import requests
from datetime import datetime, timezone, timedelta

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, 'Привет, я бот-синоптик! Напиши название своего города.')

#конвертация времени относительно часового пояса
def convert_unix_to_local_time(date_time, timezone_offset):
    dt_utc = datetime.utcfromtimestamp(date_time)
    local_timezone = timezone(timedelta(seconds=timezone_offset))
    local_time = dt_utc.replace(tzinfo=timezone.utc).astimezone(local_timezone)
    formatted_time = local_time.strftime('%Y-%m-%d %H:%M:%S')
    return formatted_time

@bot.message_handler(content_types=['text'])
def get_weather(message):
    city = message.text.strip().lower()
    res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_WHEATHER_TOKEN}&units=metric')
    
    if res.status_code == 200:
        weather = res.json()
        temp = weather["main"]["temp"]
        description = weather["weather"][0]["description"]
        description_ru = weather_descriptions.get(description, description)
        date_time = weather["dt"]
        timezone_offset = weather["timezone"]
        local_time = convert_unix_to_local_time(date_time, timezone_offset)

        bot.reply_to(message, f'Сейчас температура в {city}: {temp}°C')
        bot.send_message(message.chat.id, f'Осадки: {description_ru}')
        bot.send_message(message.chat.id, f'Местное время: {local_time}')
    elif res.status_code == 401:
        bot.reply_to(message, 'Неверный API-ключ. Пожалуйста, проверьте ваш API-ключ и попробуйте снова.')
    else:
        bot.reply_to(message, 'Не удалось получить данные о погоде. Пожалуйста, проверьте название города и попробуйте снова.')

def main():
    bot.polling(none_stop=True)

if __name__ == "__main__":
    main()

