from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from ..api.services.ai import rag_answer
import logging

logger = logging.getLogger(__name__)

ask_router = Router()

@ask_router.message(Command("ask"))
async def cmd_ask(message: Message):
    # Извлекаем вопрос после "/ask "
    question = message.text[5:].strip()
    
    if not question:
        help_text = (
            "🧠 *Как спросить ИИ?*\n\n"
            "Напишите вопрос после `/ask`:\n"
            "• `/ask Что я думал про RAG?`\n"
            "• `/ask Кратко опиши мои заметки про ИИ`\n"
            "• `/ask Какие риски у агентов?`\n\n"
            "⚠️ Ответы основаны ТОЛЬКО на ваших сохранённых заметках."
        )
        await message.answer(help_text, parse_mode="Markdown")
        return

    user_id = message.from_user.id
    logger.info(f"[RAG] Запрос от user={user_id}: '{question[:50]}...'")

    try:
        # Генерируем ответ через RAG
        answer = await rag_answer(question, user_id=user_id)
        
        # Форматируем ответ
        if "Не знаю" in answer or "извините" in answer.lower():
            response = (
                "🔍 *Не найдено релевантных заметок.*\n\n"
                "Попробуйте:\n"
                "• Сохранить больше контента через `/save`\n"
                "• Задать вопрос точнее"
            )
            await message.answer(response, parse_mode="Markdown")
        else:
            # Убираем возможные артефакты (например, "Ответ:" в начале)
            clean_answer = answer
            if clean_answer.startswith("Ответ:"):
                clean_answer = clean_answer[6:].strip()
            if clean_answer.startswith("Ответ —"):
                clean_answer = clean_answer[7:].strip()
                
            response = (
                f"🤖 *{clean_answer}*\n\n"
                "_Ответ сгенерирован на основе ваших заметок._"
            )
            await message.answer(response, parse_mode="Markdown")

        # Логируем успешный запрос
        logger.info(f"[RAG] Ответ для user={user_id}: '{answer[:60]}...'")

    except Exception as e:
        error_msg = f"⚠️ Ошибка ИИ: {str(e)[:100]}"
        logger.error(f"[RAG] Ошибка для user={user_id}: {e}")
        await message.answer(
            "❌ Не удалось обработать запрос.\n"
            "Возможно, Ollama не отвечает или модель не загружена.\n\n"
            "Проверьте: `ollama list` → должны быть `llama3.2:1b` и `nomic-embed-text`",
            parse_mode="Markdown"
        )
