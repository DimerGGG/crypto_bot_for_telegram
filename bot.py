import telebot
from extensions import APIException, CurrencyConverter
from configobj import ConfigObj


config = ConfigObj('config.ini')
BOT_TOKEN = config['DEFAULT']['BOT_TOKEN']

bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    text = ("Добро пожаловать! Чтобы узнать цену валюты, отправьте сообщение в формате:\n"
            "имя валюты, цену которой хотите узнать имя валюты, в которой надо узнать цену первой валюты количество первой валюты\n"
            "пример: USD RUB 1"
            "Для получения списка доступных валют введите команду /values")
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message):
    text = "Доступные валюты:\nЕвро (EUR)\nДоллар США (USD)\nРубль (RUB)"
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def convert(message):
    try:
        values = message.text.split()
        if len(values) != 3:
            raise APIException("Неправильное количество параметров. Формат сообщения: <валюта1> <валюта2> <количество>")

        base, quote, amount = values
        total_base = CurrencyConverter.get_price(base, quote, amount)
    except APIException as e:
        bot.reply_to(message, f"Ошибка пользователя.\n{e}")
    except Exception as e:
        bot.reply_to(message, f"Не удалось обработать команду\n{e}")
    else:
        text = f"Цена {amount} {base} в {quote} — {total_base}"
        bot.reply_to(message, text)


bot.polling()