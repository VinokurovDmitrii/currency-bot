import os
import logging
import asyncio
from datetime import datetime
from zoneinfo import ZoneInfo
import requests
from telegram import Bot
from telegram.error import TelegramError

logging.basicConfig(level=logging.INFO)

TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID_ENV = os.getenv("CHAT_ID")

if not TOKEN or not CHAT_ID_ENV:
    logging.error("Environment variables BOT_TOKEN or CHAT_ID are not set: BOT_TOKEN=%s CHAT_ID=%s", bool(TOKEN), CHAT_ID_ENV)
    raise RuntimeError("BOT_TOKEN and CHAT_ID must be set in environment")

try:
    CHAT_ID = int(CHAT_ID_ENV)
except (TypeError, ValueError):
    CHAT_ID = CHAT_ID_ENV

bot = Bot(token=TOKEN)

# Novi Sad coordinates
LAT = 45.2671
LON = 19.8335
TZ = "Europe/Belgrade"

WEATHER_CODE = {
    0: "Ясно",
    1: "Малооблачно",
    2: "Облачно",
    3: "Пасмурно",
    45: "Туман",
    48: "Морось/ледяной туман",
    51: "Лёгкий моросящий дождь",
    53: "Умеренный моросящий дождь",
    55: "Сильный моросящий дождь",
    61: "Лёгкий дождь",
    63: "Умеренный дождь",
    65: "Сильный дождь",
    71: "Снег",
    73: "Умеренный снег",
    75: "Сильный снег",
    80: "Локальные ливни",
    81: "Ливни",
    82: "Сильные ливни",
}


async def fetch_weather():
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": LAT,
        "longitude": LON,
        "current_weather": True,
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum,weathercode,time",
        "timezone": TZ,
    }
    try:
        # run blocking requests.get in a thread
        resp = await asyncio.to_thread(requests.get, url, params=params, timeout=10)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        logging.exception("Error fetching weather: %s", e)
        raise


def format_weather(data):
    now = datetime.now(ZoneInfo(TZ))
    cw = data.get("current_weather", {})
    daily = data.get("daily", {})

    temp = cw.get("temperature")
    wind = cw.get("windspeed")
    code = cw.get("weathercode")
    code_text = WEATHER_CODE.get(code, str(code))

    # find today's index in daily.time (times are in YYYY-MM-DD)
    times = daily.get("time", [])
    today_str = now.strftime("%Y-%m-%d")
    idx = 0
    if today_str in times:
        idx = times.index(today_str)

    def safe_get(arr, i):
        try:
            return arr[i]
        except Exception:
            return None

    t_max = safe_get(daily.get("temperature_2m_max", []), idx)
    t_min = safe_get(daily.get("temperature_2m_min", []), idx)
    precip = safe_get(daily.get("precipitation_sum", []), idx)
    day_code = safe_get(daily.get("weathercode", []), idx) or code
    day_text = WEATHER_CODE.get(day_code, str(day_code))

    lines = [
        f"🌤️ Погода — Нови-Сад ({now.strftime('%d.%m.%Y %H:%M',)})",
        f"Сейчас: {temp}°C, {code_text}, ветер {wind} м/с",
        "",
        "Прогноз на сегодня:",
    ]

    if t_max is not None or t_min is not None:
        lines.append(f"• Макс: {t_max}°C, Мин: {t_min}°C")
    if precip is not None:
        lines.append(f"• Ожидаемые осадки: {precip} мм")
    if day_text:
        lines.append(f"• Общее: {day_text}")

    return "\n".join(lines)


async def send_weather():
    data = await fetch_weather()
    text = format_weather(data)
    logging.info("Weather text: %s", text)
    try:
        res = await bot.send_message(chat_id=CHAT_ID, text=text)
        logging.info("Weather sent: message_id=%s", getattr(res, "message_id", None))
    except TelegramError as e:
        logging.exception("Telegram API error when sending weather: %s", e)
        raise


if __name__ == "__main__":
    asyncio.run(send_weather())
