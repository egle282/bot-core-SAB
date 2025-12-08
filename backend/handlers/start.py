from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from ..lib.analytics import capture_event
import logging

logger = logging.getLogger(__name__)

start_router = Router()

@start_router.message(Command("start"))
async def cmd_start(message: Message):
    user_id = message.from_user.id
    first_name = message.from_user.first_name or "Друг"
    
    # Отправляем приветствие
    welcome_text = (
        f"🌟 *Привет, {first_name}!* Добро пожаловать в **Bot-core-SAB**.\n\n"
        "Это ваш *ИИ-ассистент знаний* — прямо в Telegram.\n\n"
        "📌 *Как начать:*\n"
        "1️⃣ Сохраните заметку: `/save Текст` или перешлите пост + `/save`\n"
        "2️⃣ Найдите по смыслу: `/search ИИ`\n"
        "3️⃣ Спросите ИИ: `/ask Что я думал про RAG?`\n\n"
        "✨ *Особенности:*\n"
        "• Авто-аннотация и резюме\n"
        "• Семантический поиск (не по словам!)\n"
        "• Экспорт в Obsidian, Notion, PDF\n"
        "• Приватность: ваши данные — у вас\n\n"
        "🚀 *Готовы?* Просто перешлите любое сообщение и напишите `/save`!"
    )
    
    await message.answer(welcome_text, parse_mode="Markdown")
    
    # Отправляем early-bird CTA (раз в 24ч, но пока каждый раз для теста)
    early_text = (
        "🎁 *Ранний доступ:*\n"
        "Первые 100 пользователей получат **пожизненную скидку 30%**.\n\n"
        "👉 Напишите `early` — пришлю персональный QR-код для активации."
    )
    await message.answer(early_text, parse_mode="Markdown")
    
    # Логируем событие в PostHog
    try:
        await capture_event(
            distinct_id=str(user_id),
            event="bot_started",
            properties={
                "language": message.from_user.language_code or "unknown",
                "first_name": first_name,
                "is_premium": message.from_user.is_premium or False
            }
        )
        logger.info(f"[Analytics] Событие 'bot_started' отправлено для user={user_id}")
    except Exception as e:
        logger.warning(f"[Analytics] Не удалось отправить событие: {e}")
