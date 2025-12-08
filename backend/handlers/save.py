from aiogram import Router, F
from aiogram.types import Message, ContentType
from aiogram.filters import Command
from ..models import SavedItem, Session, engine
from ..api.services.ai import generate_summary, get_embedding
import json
import logging

# Настройка логгера
logger = logging.getLogger(__name__)

save_router = Router()

@save_router.message(Command("save"))
async def cmd_save(message: Message):
    user_id = message.from_user.id
    text = message.text[6:].strip()  # убираем "/save "

    content = ""
    content_type = ""
    caption = ""

    # Сценарий 1: /save с текстом
    if text:
        content = text
        content_type = "text"
        caption = message.caption or ""
    
    # Сценарий 2: пересланное сообщение
    elif message.reply_to_message:
        reply = message.reply_to_message
        
        if reply.text:
            content = reply.text
            content_type = "text"
            caption = reply.caption or ""
        
        elif reply.photo:
            # Берём самую большую версию фото
            photo = reply.photo[-1]
            content = photo.file_id
            content_type = "photo"
            caption = reply.caption or ""
        
        elif reply.document:
            content = reply.document.file_id
            content_type = "document"
            caption = reply.caption or ""
        
        elif reply.video:
            content = reply.video.file_id
            content_type = "video"
            caption = reply.caption or ""
        
        else:
            await message.answer("❌ Поддерживаются: текст, фото, документы, видео.")
            return
    
    # Сценарий 3: ничего не передано
    else:
        await message.answer(
            "📌 Как сохранить:\n"
            "• Напишите `/save Текст заметки`\n"
            "• Или перешлите сообщение и напишите `/save`"
        )
        return

    # --- AI-обработка: аннотация и эмбеддинги ---
    summary = ""
    embedding_json = json.dumps([0.0] * 384)  # fallback — 384-dim для nomic-embed-text (урезанный)

    try:
        # Генерация краткого резюме
        summary = await generate_summary(content)
        logger.info(f"[AI] Сгенерировано резюме для user={user_id}: {summary[:50]}...")

        # Получение эмбеддингов
        embedding = await get_embedding(content)
        embedding_json = json.dumps(embedding)

    except Exception as e:
        logger.error(f"[AI] Ошибка при обработке для user={user_id}: {e}")
        # Не прерываем сохранение — работаем без AI
        summary = ""
        embedding_json = json.dumps([0.0] * 384)

    # --- Сохранение в БД ---
    try:
        with Session(engine) as session:
            item = SavedItem(
                user_id=user_id,
                content_type=content_type,
                content=content,
                caption=caption,
                summary=summary,
                embedding=embedding_json,
                tags=""
            )
            session.add(item)
            session.commit()
            item_id = item.id

        logger.info(f"[DB] Сохранено: id={item_id}, user={user_id}, type={content_type}")

    except Exception as e:
        logger.error(f"[DB] Ошибка сохранения для user={user_id}: {e}")
        await message.answer("⚠️ Не удалось сохранить. Попробуйте позже.")
        return

    # --- Ответ пользователю ---
    response_lines = ["✅ Сохранено!"]

    if summary:
        preview = summary[:70] + ("…" if len(summary) > 70 else "")
        response_lines.append(f"📝 Кратко: *{preview}*")

    if content_type in ("photo", "document", "video"):
        response_lines.append(f"📎 Тип: {content_type}")

    response_lines.append("")
    response_lines.append("🔍 Искать: `/search тема`")
    response_lines.append("🧠 Спросить ИИ: `/ask вопрос`")

    await message.answer(
        "\n".join(response_lines),
        parse_mode="Markdown"
    )
