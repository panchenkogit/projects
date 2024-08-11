from os import error
import telebot
from telebot  import types
from currency_converter import CurrencyConverter

bot = telebot.TeleBot('')
currency = CurrencyConverter()
amount = 0

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id,'Привет,введите сумму:')
    bot.register_next_step_handler(message, sum)
    
def sum(message):
    global amount    
    try:
        amount = int(message.text.strip())
    except ValueError:
        bot.send_message(message.chat.id, 'Неверный формат,введите сумму заново.')
        bot.register_next_step_handler(message, sum)
        return
    if amount >0:
        markup = types.InlineKeyboardMarkup(row_width=2)
        USD_RUB = types.InlineKeyboardButton('USD/RUB', callback_data='usd/rub')
        RUB_USD = types.InlineKeyboardButton('RUB/USD', callback_data='rub/usd')
        USD_EUR = types.InlineKeyboardButton('USD/EUR', callback_data='usd/eur')
        other = types.InlineKeyboardButton('Другое значение', callback_data='else')
        markup.add(USD_EUR,USD_RUB,RUB_USD,other)
        bot.send_message(message.chat.id, 'Выберте пару валют', reply_markup=markup)
    else:
        bot.send_message(message.chat.id, 'Введите сумму больше 0.')
        bot.register_next_step_handler(message, sum)
        
@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data != 'else':
        values = call.data.upper().split('/')
        res = currency.convert(amount, values[0],values[1])
        bot.send_message(call.message.chat.id, f'Получается: {round(res,2)}')
        bot.register_next_step_handler(call.message, sum)
    else:
        bot.send_message(call.message.chat.id, 'Введите пару значений через /')
        bot.register_next_step_handler(call.message, my_currency)
        
def my_currency(message):
    values = message.text.upper().split('/')
    try:
        res = currency.convert(amount, values[0],values[1])
        bot.send_message(message.chat.id, f'Получается: {round(res,2)}.Можете снова ввести сумму.')
        bot.register_next_step_handler(message, sum)
    except:
        bot.send_message(message.chat.id, 'Что то пошло не так.Попробуйте снова.')
        bot.register_next_step_handler(message, sum)
    
def main():
    bot.polling(none_stop=True)
    
if __name__ == "__main__":
    main()
