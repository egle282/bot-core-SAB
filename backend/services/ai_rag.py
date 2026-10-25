import json
import logging
import httpx
from math import sqrt
from typing import List, Any
from .ai_config import OLLAMA_URL, SUMMARY_MODEL
from .ai_embeddings import get_embedding

logger = logging.getLogger(__name__)

def cosine_similarity(a: List[float], b: List[float]) -> float:
    """Косинусное сходство между двумя векторами"""
    if not a or not b:
        return 0.0
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = sqrt(sum(x * x for x in a))
    norm_b = sqrt(sum(x * x for x in b))
    return dot / (norm_a * norm_b) if norm_a > 0 and norm_b > 0 else 0.0


async def semantic_search(query: str, user_id: int, top_k: int = 3) -> List[Any]:
    """
    Семантический поиск по эмбеддингам заметок пользователя в базе данных.
    """
    try:
        from ..models import SavedItem, Session, engine
    except (ImportError, ValueError):
        from models import SavedItem, Session, engine

    try:
        query_emb = await get_embedding(query)
        
        with Session(engine) as session:
            items = session.query(SavedItem).filter(
                SavedItem.user_id == user_id,
                SavedItem.embedding.isnot(None)
            ).all()

        scored = []
        for item in items:
            try:
                item_emb = json.loads(item.embedding) if item.embedding else []
                if len(item_emb) == len(query_emb):
                    score = cosine_similarity(query_emb, item_emb)
                    if score > 0.3:
                        scored.append((score, item))
            except (json.JSONDecodeError, TypeError, ValueError):
                continue

        scored.sort(key=lambda x: x[0], reverse=True)
        return [item for _, item in scored[:top_k]]

    except Exception as e:
        logger.error(f"[AI] Ошибка семантического поиска: {e}")
        return []


async def rag_answer(question: str, user_id: int) -> str:
    """
    Генерирует ответ на вопрос пользователя через RAG на основе его заметок.
    """
    try:
        relevant_items = await semantic_search(question, user_id, top_k=3)
        if not relevant_items:
            return "Не знаю. У меня нет релевантных заметок по этому вопросу."

        context_parts = []
        for i, item in enumerate(relevant_items, 1):
            text = getattr(item, "summary", "") or getattr(item, "content", "") or ""
            context_parts.append(f"{i}. {text}")
        context = "\n".join(context_parts)

        prompt = (
            "Ответь на вопрос, используя ТОЛЬКО информацию из контекста ниже. "
            "Если в контексте нет ответа — скажи 'Не знаю'.\n\n"
            f"Контекст:\n{context}\n\n"
            f"Вопрос: {question}\n"
            "Ответ (на русском, кратко):"
        )

        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                f"{OLLAMA_URL}/api/generate",
                json={
                    "model": SUMMARY_MODEL,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.1,
                        "num_predict": 150
                    }
                }
            )
            response.raise_for_status()
            result = response.json()
            answer = result.get("response", "").strip()
            return answer if answer else "Не знаю."

    except Exception as e:
        logger.error(f"[AI] Ошибка RAG: {e}")
        return "Извините, не могу ответить сейчас."
