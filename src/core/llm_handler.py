"""
llm_handler.py: مسؤول عن التواصل مع الـ LLM
يدعم Groq و Gemini
"""

from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
from src.utils.logger import get_logger
from src.utils.config import settings

logger = get_logger(__name__)


class LLMHandler:
    """
    يوفر LLM جاهز للاستخدام
    بناءً على المزود المختار
    """

    def get_llm(self, provider: str = "groq"):
        """
        provider = "groq" أو "gemini"
        يرجع LLM جاهز للاستخدام
        """

        if provider == "groq":
            return self._get_groq()
        elif provider == "gemini":
            return self._get_gemini()
        else:
            # لو كتب اسم غلط نرجع groq افتراضياً
            logger.warning(f"مزود غير معروف: {provider}، نستخدم Groq")
            return self._get_groq()

    def _get_groq(self):
        """إعداد Groq LLM"""
        logger.info(f"تحميل Groq: {settings.groq_model}")

        return ChatGroq(
            groq_api_key=settings.groq_api_key,
            model_name=settings.groq_model,
            # 0.1 = إجابات دقيقة وثابتة
            # قريب من 1 = إبداعي لكن أقل دقة
            temperature=settings.temperature,
            max_tokens=settings.max_tokens
        )

    def _get_gemini(self):
        """إعداد Gemini LLM"""
        logger.info(f"تحميل Gemini: {settings.gemini_model}")

        return ChatGoogleGenerativeAI(
            google_api_key=settings.gemini_api_key,
            model=settings.gemini_model,
            temperature=settings.temperature,
            max_output_tokens=settings.max_tokens
        )