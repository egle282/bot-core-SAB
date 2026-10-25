import httpx
import logging
from .ai_config import OLLAMA_URL, SUMMARY_MODEL

logger = logging.getLogger(__name__)

async def generate_summary(text: str, max_length: int = 500) -> str:
    """
    Генерирует 1-предложение резюме текста через Ollama.
    Fallback: возвращает первые 100 символов.
    """
    if not text.strip():
        return ""

    try:
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
                        "num_predict": 100
                    }
                }
            )
            response.raise_for_status()
            result = response.json()
            
            summary = result.get("response", "").strip()
            if summary.startswith("Кратко: "):
                summary = summary[8:]
            if summary.endswith("."):
                summary = summary[:-1]
                
            logger.info(f"[AI] Сгенерировано резюме ({len(summary)} симв.): {summary[:60]}...")
            return summary

    except Exception as e:
        logger.warning(f"[AI] Ошибка генерации резюме (используем fallback): {e}")
        fallback = text[:100].strip()
        if len(text) > 100:
            fallback += "..."
        return fallback
