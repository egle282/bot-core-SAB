import asyncio
import json
import os
import sys

# Обеспечиваем доступность модулей backend при прямом запуске
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from services.ai import generate_summary, get_embedding, rag_answer
from models import SavedItem, Session, engine

os.environ.setdefault("OLLAMA_URL", "http://localhost:11434")

async def test():
    text = "В 2025 году вышел бот SaveAsBot, который позволяет сохранять контент в Telegram и искать по смыслу."
    
    print("--- 1. Тест summary ---")
    summary = await generate_summary(text)
    print("✅ Результат:", summary)
    
    print("\n--- 2. Тест embedding ---")
    emb = await get_embedding(text)
    print("✅ Размер вектора:", len(emb))
    
    # Сохраняем тестовую заметку для проверки RAG
    with Session(engine) as session:
        item = SavedItem(
            user_id=123,
            content_type="text",
            content=text,
            summary=summary,
            embedding=json.dumps(emb)
        )
        session.add(item)
        session.commit()
    
    print("\n--- 3. Тест RAG ---")
    answer = await rag_answer("Что делает SaveAsBot?", user_id=123)
    print("✅ Ответ:", answer)

if __name__ == "__main__":
    asyncio.run(test())
