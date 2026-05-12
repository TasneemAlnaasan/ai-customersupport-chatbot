"""
llm_handler.py: مسؤول عن التواصل مع Groq
"""

from langchain_groq import ChatGroq
from src.utils.logger import get_logger
from src.utils.config import settings

logger = get_logger(__name__)


class LLMHandler:

    def get_llm(self, provider: str = "groq"):
        return self._get_groq()

    def _get_groq(self):
        logger.info(f"تحميل Groq: {settings.groq_model}")
        return ChatGroq(
            groq_api_key=settings.groq_api_key,
            model_name=settings.groq_model,
            temperature=settings.temperature,
            max_tokens=settings.max_tokens
        )