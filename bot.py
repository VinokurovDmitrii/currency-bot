import os
import requests
from telegram import Bot
from telegram.error import BadRequest, TelegramError
from datetime import datetime
from zoneinfo import ZoneInfo

TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = int(os.getenv("CHAT_ID"))
MESSAGE_ID = int(os.getenv("MESSAGE_ID"))

bot = Bot(token=TOKEN)

# Месяцы на русском
MONTHS_RU = [
    "января", "февраля", "марта", "апреля", "мая", "июня",
    "июля", "августа", "сентября", "октября", "ноября", "декабря"
]

def get_rates():
    url = "https://www.cbr-xml-daily.ru/daily_json.js"
    try:
        data = requests.get(url, timeout=10).json()
        usd = data["Valute"]["USD"]["Value"]
        eur = data["Valute"]["EUR"]["Value"]
        return usd, eur
    except (requests.RequestException, KeyError) as e:
        print(f"Ошибка при получении курса: {e}")
        return None, None

def main():
    usd, eur = get_rates()
    if usd is None or eur is None:
        return  # не продолжаем, если ошибка с курсами

    # get current time in Belgrade timezone
    tz = ZoneInfo("Europe/Belgrade")
    now = datetime.now(tz)
    day = now.day
    month = MONTHS_RU[now.month - 1]  # месяц по-русски
    hour = now.hour
    minute = now.minute

    text = (
        f"🇪🇺 EUR: {eur:.2f} ₽\n"
        f"🇺🇸 USD: {usd:.2f} ₽\n\n"
        f"🕒 Актуально на {day} {month} {hour:02d}:{minute:02d}"
    )

    try:
        bot.edit_message_text(chat_id=CHAT_ID, message_id=MESSAGE_ID, text=text)
    except BadRequest as e:
        if "Message is not modified" in str(e):
            print("Сообщение не изменилось, ничего не делаем")
        else:
            raise
    except TelegramError as e:
        print(f"Ошибка Telegram API: {e}")

if __name__ == "__main__":
    main()
