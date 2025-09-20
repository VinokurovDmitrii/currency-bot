# 📦 Currency & Predictions Bot

Коротко: бот публикует курсы валют и случайные предсказания в Telegram. Запускается из GitHub Actions.

Файлы:
- `bot.py` — публикует/редактирует курс (CBR).
- `predictions.py` — отправляет случайное предсказание.

Настройка (быстро):
1. Создать секреты в GitHub → Settings → Secrets:
   - `BOT_TOKEN` — токен от BotFather
   - `CHAT_ID` — id чата (для супергрупп `-100...` или `@channelname`)
   - (опционально) `MESSAGE_ID` — id сообщения для редактирования в `bot.py`

Запуск локально:
```bash
python3 -m venv venv
source venv/bin/activate
pip install python-telegram-bot
export BOT_TOKEN="123:ABC"
export CHAT_ID="-100123..."
python3 -u predictions.py
```

Отладка:
- Проверьте, что бот добавлен в чат и может писать.
- Получить chat id:
  ```bash
  curl -s "https://api.telegram.org/bot$BOT_TOKEN/getUpdates" | jq .
  ```
- В логах Action теперь виден выбор предсказания и результат `send_message`.

Ошибки:
- `BadRequest: chat not found` — неверный `CHAT_ID` или бот не в чате.
- `Unauthorized` — неверный `BOT_TOKEN`.
- `Forbidden` — бот заблокирован или нет прав.

Примечание: список предсказаний содержит нецензурную лексику — замените при необходимости.

Хочешь — добавлю `.gitignore` и `requirements.txt` и закоммичу. 👍
