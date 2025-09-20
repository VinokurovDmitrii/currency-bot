# 💱 Telegram Currency Bot (GitHub Actions)

Этот бот раз в час обновляет одно сообщение в чате Telegram, показывая курс USD и EUR к рублю (по данным ЦБ РФ).

---

## 🚀 Установка

1. Создай бота в [@BotFather](https://t.me/BotFather) → получи `BOT_TOKEN`.
2. Добавь бота в группу → узнай `CHAT_ID` через `getUpdates`.
3. Отправь первое сообщение вручную:
   ```
   https://api.telegram.org/bot<BOT_TOKEN>/sendMessage?chat_id=<CHAT_ID>&text=Инициализация
   ```
   Скопируй `message_id` из ответа.
4. В репозитории → Settings → Secrets → Actions:
   - `BOT_TOKEN` = токен бота
   - `CHAT_ID` = id группы (с минусом, например `-1001234567890`)
   - `MESSAGE_ID` = id сообщения
5. GitHub Actions сам будет запускать `bot.py` каждый час и обновлять сообщение.

---

## 🛠 Ручной запуск
Можно запустить workflow вручную (Actions → Run workflow), если нужно обновить курсы прямо сейчас.
