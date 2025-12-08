from aiogram import Router, F
from aiogram.types import Message, ContentType
from aiogram.filters import Command
from ..models import SavedItem, Session, engine
from ..api.services.ai import generate_summary, get_embedding
import json

save_router = Router()

@save_router.message(Command("save"))
async def cmd_save(message: Message):
    user_id = message.from_user.id
    text = message.text[6:].strip()  # убираем "/save "

    # Если после /save есть текст — сохраняем его
    if text:
        content = text
        content_type = "text"
        caption = message.caption or ""
    # Если переслано сообщение — берём его содержимое
    elif message.reply_to_message:
        reply = message.reply_to_message
        if reply.text:
            content = reply.text
            content_type = "text"
            caption = reply.caption or ""
        elif reply.photo:
            photo = reply.photo[-1]  # самое большое
            content = photo.file_id
            content_type = "photo"
            caption = reply.caption or ""
        elif reply.document:
            content = reply.document.file_id
            content_type = "document"
            caption = reply.caption or ""
        else:
            await message.answer("❌ Поддерживаются: текст, фото, документы.")
            return
    else:
        await message.answer("📌 Отправьте текст или перешлите сообщение после /save")
        return

    # --- AI-обработка ---
    try:
        summary = await generate_summary(content)
        embedding = await get_embedding(content)
    except Exception as e:
        print(f"[AI] Ошибка: {e}")
        summary = ""
        embedding = json.dumps([0.0] * 384)

    # --- Сохранение ---
    with Session(engine) as session:
        item = SavedItem(
            user_id=user_id,
            content_type=content_type,
            content=content,
            caption=caption,
            summary=summary,
            embedding=embedding,
            tags=""
        )
        session.add(item)
        session.commit()
        item_id = item.id

    await message.answer(
        f"✅ Сохранено!\n"
        f"📝 Кратко: {summary[:60]}...\n"
        f"🔍 Искать: `/search тема` или `/ask вопрос`"
    )
