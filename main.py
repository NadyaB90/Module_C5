import telebot
from extensions import APIException, Converter
from config import *
import traceback

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def hello(message: telebot.types.Message):
    text = 'Чтобы узнать курс валют, введите команду боту в следующем порядке: <имя валюты> <в какую валюту перевести> <количество переводимой валюты> ' \
           '\n Чтобы узнать список достуных валют, нажмите /values'
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for i in exchanges.keys():
        text = '\n'.join((text, i))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text'])
def converter(message: telebot.types.Message):
    values_1 = message.text.split()
    try:
        if len(values_1) != 3:
            raise APIException('Неверное количество параметров!')
        
        answer = Converter.get_price(*values_1)
    except APIException as e:
        bot.reply_to(message, f"Ошибка в команде:\n{e}" )
    except Exception as e:
        traceback.print_tb(e.__traceback__)
        bot.reply_to(message, f"Неизвестная ошибка:\n{e}" )
    else:
        bot.reply_to(message,answer)

bot.polling()
