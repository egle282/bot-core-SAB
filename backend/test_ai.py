import asyncio
import os
from api.services.ai import generate_summary, get_embedding, rag_answer
from models import SavedItem, Session, engine

os.environ["OLLAMA_URL"] = "http://localhost:11434"

async def test():
    text = "В 2025 году вышел бот SaveAsBot, который позволяет сохранять контент в Telegram и искать по смыслу."
    
    print("Тест summary...")
    summary = await generate_summary(text)
    print("✅", summary)
    
    print("\nТест embedding...")
    emb = await get_embedding(text)
    print("✅ Размер:", len(emb))
    
    # Сохраним тестовую заметку для RAG
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
    
    print("\nТест RAG...")
    answer = await rag_answer("Что делает SaveAsBot?", user_id=123)
    print("✅", answer)

if __name__ == "__main__":
    asyncio.run(test())
