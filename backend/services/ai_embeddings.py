import httpx
import logging
from typing import List
from .ai_config import OLLAMA_URL, EMBEDDING_MODEL, VALID_EMBEDDING_SIZES, FALLBACK_EMBEDDING_SIZE

logger = logging.getLogger(__name__)

async def get_embedding(text: str) -> List[float]:
    """
    Получает эмбеддинг текста через Ollama.
    Fallback: возвращает нулевой вектор нужной длины (384).
    """
    if not text.strip():
        target_size = VALID_EMBEDDING_SIZES.get(EMBEDDING_MODEL, FALLBACK_EMBEDDING_SIZE)
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

            # Нормализация длины вектора до 384
            if len(embedding) > 384:
                embedding = embedding[:384]
            elif len(embedding) < 384:
                embedding += [0.0] * (384 - len(embedding))
                
            logger.info(f"[AI] Получен эмбеддинг (размер: {len(embedding)})")
            return embedding

    except Exception as e:
        logger.warning(f"[AI] Ошибка эмбеддинга (используем fallback): {e}")
        return [0.0] * 384
