import os
import logging
from typing import List

logger = logging.getLogger(__name__)

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
SUMMARY_MODEL = os.getenv("SUMMARY_MODEL", os.getenv("MODEL_NAME", "llama3.2:1b"))
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "nomic-embed-text")

# Валидные длины эмбеддингов
VALID_EMBEDDING_SIZES = {
    "nomic-embed-text": 768,
    "all-minilm": 384,
    "mxbai-embed-large": 1024,
}
FALLBACK_EMBEDDING_SIZE = 384
