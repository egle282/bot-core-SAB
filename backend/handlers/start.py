from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
import logging

try:
    from ..lib.analytics import capture_event
except (ImportError, ValueError):
    from lib.analytics import capture_event

logger = logging.getLogger(__name__)

start_router = Router()

@start_router.message(Command("start"))
async def cmd_start(message: Message):
    user_id = message.from_user.id if message.from_user else 0
    first_name = (message.from_user.first_name if message.from_user else None) or "Друг"
    
    welcome_text = (
        f"🌟 *Привет, {first_name}!* Добро пожаловать в **SaveAs Pro**.\n\n"
        "Это ваш *ИИ-ассистент знаний* — прямо в Telegram.\n\n"
        "📌 *Как начать:*\n"
        "1️⃣ Сохраните заметку: `/save Текст` или перешлите пост + `/save`\n"
        "2️⃣ Найдите по смыслу: `/search ИИ`\n"
        "3️⃣ Спросите ИИ: `/ask Что я думал про RAG?`\n\n"
        "✨ *Особенности:*\n"
        "• Авто-аннотация и резюме\n"
        "• Семантический поиск (по смыслу, а не словам)\n"
        "• Приватность: ваши данные хранятся локально\n\n"
        "🚀 *Готовы?* Просто перешлите любое сообщение и напишите `/save`!"
    )
    await message.answer(welcome_text, parse_mode="Markdown")
    
    early_text = (
        "🎁 *Ранний доступ:*\n"
        "Первые 100 пользователей получат **пожизненную скидку 30%**.\n\n"
        "👉 Напишите `early` — пришлю персональный QR-код для активации."
    )
    await message.answer(early_text, parse_mode="Markdown")
    
    try:
        await capture_event(
            distinct_id=str(user_id),
            event="bot_started",
            properties={
                "language": (message.from_user.language_code if message.from_user else "unknown") or "unknown",
                "first_name": first_name,
                "is_premium": (message.from_user.is_premium if message.from_user else False) or False
            }
        )
        logger.info(f"[Analytics] Событие 'bot_started' отправлено для user={user_id}")
    except Exception as e:
        logger.warning(f"[Analytics] Не удалось отправить событие: {e}")
