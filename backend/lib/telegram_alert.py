from aiogram import Bot
import os

ALERT_CHAT_ID = os.getenv("ALERT_CHAT_ID")
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if BOT_TOKEN and ALERT_CHAT_ID:
    bot = Bot(token=BOT_TOKEN)
else:
    bot = None

async def send_alert_to_admin(text: str):
    if not bot:
        print("[Telegram] Не настроен бот или chat_id")
        return
    
    try:
        await bot.send_message(
            chat_id=int(ALERT_CHAT_ID),
            text=text,
            disable_notification=False
        )
    except Exception as e:
        print(f"[Telegram Alert] Ошибка: {e}")
