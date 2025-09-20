import os
import requests
from telegram import Bot

TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = int(os.getenv("CHAT_ID"))
bot = Bot(token=TOKEN)

def get_rates():
    url = "https://www.cbr-xml-daily.ru/daily_json.js"
    r = requests.get(url)
    data = r.json()
    usd = data["Valute"]["USD"]["Value"]
    eur = data["Valute"]["EUR"]["Value"]
    return usd, eur

def send_rates():
    usd, eur = get_rates()
    text = f"💵 Курс валют на сегодня:\n1 USD = {usd:.2f}₽\n1 EUR = {eur:.2f}₽"
    bot.send_message(chat_id=CHAT_ID, text=text)

if __name__ == "__main__":
    send_rates()
