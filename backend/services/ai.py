import os
import json
import httpx
from typing import List, Union
import logging

logger = logging.getLogger(__name__)

# Настройки из .env
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
SUMMARY_MODEL = os.getenv("SUMMARY_MODEL", "llama3.2:1b")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "nomic-embed-text")

# Валидные длины эмбеддингов (для fallback)
VALID_EMBEDDING_SIZES = {
    "nomic-embed-text": 768,
    "all-minilm": 384,
    "mxbai-embed-large": 1024,
}
FALLBACK_SIZE = 384  # Используем усечённый размер для экономии места


async def generate_summary(text: str, max_length: int = 500) -> str:
    """
    Генерирует 1-предложение резюме текста.
    Fallback: возвращает первые 100 символов.
    """
    if not text.strip():
        return ""

    try:
        # Ограничиваем длину для экономии токенов
        prompt = f"Кратко (ровно 1 предложение, без форматирования, на русском): {text[:max_length]}"
        
        async with httpx.AsyncClient(timeout=45.0) as client:
            response = await client.post(
                f"{OLLAMA_URL}/api/generate",
                json={
                    "model": SUMMARY_MODEL,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.3,
                        "num_predict": 100  # ограничение длины ответа
                    }
                }
            )
            response.raise_for_status()
            result = response.json()
            
            summary = result.get("response", "").strip()
            # Очищаем от артефактов
            if summary.startswith("Кратко: "):
                summary = summary[8:]
            if summary.endswith("."):
                summary = summary[:-1]
                
            logger.info(f"[AI] Сгенерировано резюме ({len(summary)} симв.): {summary[:60]}...")
            return summary

    except Exception as e:
        logger.warning(f"[AI] Ошибка генерации резюме (используем fallback): {e}")
        # Fallback: первые 100 символов + "..."
        fallback = text[:100].strip()
        if len(text) > 100:
            fallback += "..."
        return fallback


async def get_embedding(text: str) -> List[float]:
    """
    Получает эмбеддинг текста через Ollama.
    Fallback: возвращает нулевой вектор нужной длины.
    """
    if not text.strip():
        # Пустой текст → нулевой вектор
        target_size = VALID_EMBEDDING_SIZES.get(EMBEDDING_MODEL, FALLBACK_SIZE)
        return [0.0] * target_size

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{OLLAMA_URL}/api/embeddings",
                json={
                    "model": EMBEDDING_MODEL,
                    "prompt": text
                }
            )
            response.raise_for_status()
            data = response.json()
            
            embedding = data.get("embedding")
            if not isinstance(embedding, list) or len(embedding) == 0:
                raise ValueError("Пустой эмбеддинг")

            # Уменьшаем до 384 для экономии места в SQLite (nomic даёт 768)
            if len(embedding) > 384:
                embedding = embedding[:384]
            elif len(embedding) < 384:
                # Дополняем нулями
                embedding += [0.0] * (384 - len(embedding))
                
            logger.info(f"[AI] Получен эмбеддинг (размер: {len(embedding)})")
            return embedding

    except Exception as e:
        logger.warning(f"[AI] Ошибка эмбеддинга (используем fallback): {e}")
        # Fallback: нулевой вектор длиной 384
        return [0.0] * 384


# === Дополнительно: семантический поиск (можно вынести в отдельный файл) ===
async def semantic_search(query: str, user_id: int, top_k: int = 3) -> List:
    """
    Простой семантический поиск по эмбеддингам (для SQLite).
    Возвращает список SavedItem.
    """
    from math import sqrt
    from ..models import SavedItem, Session, engine

    def cosine_sim(a: List[float], b: List[float]) -> float:
        """Косинусное сходство между двумя векторами"""
        if not a or not b:
            return 0.0
        dot = sum(x * y for x, y in zip(a, b))
        norm_a = sqrt(sum(x * x for x in a))
        norm_b = sqrt(sum(x * x for x in b))
        return dot / (norm_a * norm_b) if norm_a > 0 and norm_b > 0 else 0.0

    try:
        # Получаем эмбеддинг запроса
        query_emb = await get_embedding(query)
        
        # Загружаем все заметки пользователя
        with Session(engine) as session:
            items = session.query(SavedItem).filter(
                SavedItem.user_id == user_id,
                SavedItem.embedding.isnot(None)
            ).all()

        # Считаем сходство
        scored = []
        for item in items:
            try:
                item_emb = json.loads(item.embedding) if item.embedding else []
                if len(item_emb) == len(query_emb):
                    score = cosine_sim(query_emb, item_emb)
                    if score > 0.3:  # порог релевантности
                        scored.append((score, item))
            except (json.JSONDecodeError, TypeError, ValueError):
                continue

        # Сортируем по убыванию
        scored.sort(key=lambda x: x[0], reverse=True)
        return [item for _, item in scored[:top_k]]

    except Exception as e:
        logger.error(f"[AI] Ошибка семантического поиска: {e}")
        return []


# === Дополнительно: RAG-ответ (можно вынести в отдельный файл) ===
async def rag_answer(question: str, user_id: int) -> str:
    """
    Генерирует ответ на вопрос на основе заметок пользователя.
    """
    try:
        # Ищем релевантные заметки
        relevant_items = await semantic_search(question, user_id, top_k=3)
        
        if not relevant_items:
            return "Не знаю. У меня нет релевантных заметок по этому вопросу."

        # Формируем контекст
        context_parts = []
        for i, item in enumerate(relevant_items, 1):
            text = item.summary or item.content or ""
            context_parts.append(f"{i}. {text}")
        context = "\n".join(context_parts)

        # Формируем промпт
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
