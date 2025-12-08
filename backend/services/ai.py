import os
import json
import httpx
from typing import List
from ..models import SavedItem, Session, engine
from sqlmodel import select

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
MODEL_NAME = os.getenv("MODEL_NAME", "llama3.2:1b")

async def generate_summary(text: str) -> str:
    prompt = f"Кратко (1 предложение, без форматирования): {text[:500]}"
    async with httpx.AsyncClient(timeout=30.0) as client:
        r = await client.post(
            f"{OLLAMA_URL}/api/generate",
            json={
                "model": MODEL_NAME,
                "prompt": prompt,
                "stream": False,
                "options": {"temperature": 0.3}
            }
        )
        r.raise_for_status()
        return r.json()["response"].strip()

async def get_embedding(text: str) -> str:
    async with httpx.AsyncClient(timeout=30.0) as client:
        r = await client.post(
            f"{OLLAMA_URL}/api/embeddings",
            json={"model": "nomic-embed-text", "prompt": text}
        )
        r.raise_for_status()
        emb = r.json()["embedding"]
        # Уменьшаем до 384 для экономии места (nomic даёт 768)
        return json.dumps(emb[:384])

async def semantic_search(query: str, user_id: int, top_k: int = 3) -> List[SavedItem]:
    # Получаем эмбеддинг запроса
    query_emb = json.loads(await get_embedding(query))
    
    with Session(engine) as session:
        items = session.exec(
            select(SavedItem).where(SavedItem.user_id == user_id)
        ).all()
    
    # Простой косинусный поиск (для SQLite)
    from math import sqrt
    
    def cosine_sim(a, b):
        dot = sum(x*y for x, y in zip(a, b))
        na = sqrt(sum(x*x for x in a))
        nb = sqrt(sum(x*x for x in b))
        return dot / (na * nb) if na and nb else 0
    
    scored = []
    for item in items:
        if item.embedding:
            try:
                item_emb = json.loads(item.embedding)
                score = cosine_sim(query_emb, item_emb)
                scored.append((score, item))
            except:
                continue
    
    scored.sort(key=lambda x: x[0], reverse=True)
    return [item for _, item in scored[:top_k]]

async def rag_answer(question: str, user_id: int) -> str:
    # Ищем релевантные заметки
    relevant = await semantic_search(question, user_id, top_k=3)
    context = "\n".join([
        f"- {item.summary or item.content}" for item in relevant
    ])
    
    prompt = (
        f"Ответь на вопрос, используя ТОЛЬКО контекст ниже. "
        f"Если информации нет — скажи 'Не знаю'.\n\n"
        f"Контекст:\n{context}\n\n"
        f"Вопрос: {question}\nОтвет:"
    )
    
    async with httpx.AsyncClient(timeout=60.0) as client:
        r = await client.post(
            f"{OLLAMA_URL}/api/generate",
            json={
                "model": MODEL_NAME,
                "prompt": prompt,
                "stream": False,
                "options": {"temperature": 0.1}
            }
        )
        r.raise_for_status()
        return r.json()["response"].strip()
