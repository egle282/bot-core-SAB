from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from ..models import SavedItem, Session, engine
from ..api.services.ai import semantic_search
from typing import List

search_router = Router()

@search_router.message(Command("search"))
async def cmd_search(message: Message):
    query = message.text[8:].strip()
    if not query:
        await message.answer("🔍 Введите слово после /search")
        return

    user_id = message.from_user.id
    with Session(engine) as session:
        # Сначала — текстовый поиск
        results_text = session.query(SavedItem).filter(
            SavedItem.user_id == user_id,
            SavedItem.content.contains(query)
        ).order_by(SavedItem.created_at.desc()).limit(3).all()

        # Затем — семантический (по эмбеддингам)
        try:
            results_semantic = await semantic_search(query, user_id, top_k=2)
        except Exception as e:
            print(f"[Search] Semantic error: {e}")
            results_semantic = []

        # Объединяем, убираем дубли
        seen = set()
        combined: List[SavedItem] = []
        for r in results_text + results_semantic:
            if r.id not in seen:
                seen.add(r.id)
                combined.append(r)

        if not combined:
            await message.answer("❌ Ничего не найдено.")
            return

        parts = []
        for i, r in enumerate(combined[:5], 1):
            preview = (r.summary or r.content or "")[:50].replace("\n", " ")
            parts.append(f"{i}. {preview}...")

        await message.answer("🔍 Найдено:\n" + "\n".join(parts))
