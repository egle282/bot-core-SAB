"""
Unified AI service facade (ReFF-compliant).
"""
from .ai_config import (
    OLLAMA_URL,
    SUMMARY_MODEL,
    EMBEDDING_MODEL,
    VALID_EMBEDDING_SIZES,
    FALLBACK_EMBEDDING_SIZE,
)
from .ai_summary import generate_summary
from .ai_embeddings import get_embedding
from .ai_rag import semantic_search, rag_answer, cosine_similarity

__all__ = [
    "OLLAMA_URL",
    "SUMMARY_MODEL",
    "EMBEDDING_MODEL",
    "VALID_EMBEDDING_SIZES",
    "FALLBACK_EMBEDDING_SIZE",
    "generate_summary",
    "get_embedding",
    "semantic_search",
    "rag_answer",
    "cosine_similarity",
]
