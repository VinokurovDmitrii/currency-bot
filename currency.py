import os
import requests
from telegram import Bot

TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = int(os.getenv("CHAT_ID"))

bot = Bot(token=TOKEN)

def get_rates():
    url = "https://api.exchangerate.host/latest?base=USD&symbols=RUB,EUR"
    response = requests.get(url).json()
    usd_rub = response["rates"]["RUB"]
    usd_eur = response["rates"]["EUR"]
    return usd_rub, usd_eur

def send_rates():
    usd_rub, usd_eur = get_rates()
    text = f"💵 Курс валют:\n1 USD = {usd_rub:.2f} RUB\n1 USD = {usd_eur:.2f} EUR"
    bot.send_message(chat_id=CHAT_ID, text=text)

if __name__ == "__main__":
    send_rates()
