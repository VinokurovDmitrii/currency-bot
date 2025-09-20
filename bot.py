import os
import requests
from telegram import Bot

TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = int(os.getenv("CHAT_ID"))
MESSAGE_ID = int(os.getenv("MESSAGE_ID"))

bot = Bot(token=TOKEN)

def get_rates():
    url = "https://www.cbr-xml-daily.ru/daily_json.js"
    data = requests.get(url).json()
    usd = data["Valute"]["USD"]["Value"]
    eur = data["Valute"]["EUR"]["Value"]
    return usd, eur

def main():
    usd, eur = get_rates()
    text = (
        "💱 Курсы валют (ЦБ РФ)\n\n"
        f"🇺🇸 USD: {usd:.2f} ₽\n"
        f"🇪🇺 EUR: {eur:.2f} ₽"
    )
    bot.edit_message_text(chat_id=CHAT_ID, message_id=MESSAGE_ID, text=text)

if __name__ == "__main__":
    main()
