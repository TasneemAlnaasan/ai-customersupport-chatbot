"""
chat.py: مسار المحادثة الرئيسي
"""

from fastapi import APIRouter, HTTPException
from src.api.models import ChatRequest, ChatResponse
from src.utils.logger import get_logger

logger = get_logger(__name__)
router = APIRouter()

# نحفظ RAG Pipeline في الذاكرة
# حتى لا ننشئه من جديد كل طلب
rag_pipelines = {}


def get_rag_pipeline(provider: str):
    """
    يرجع RAG Pipeline جاهز
    ينشئه فقط أول مرة
    """
    if provider not in rag_pipelines:
        from src.core.rag_pipeline import RAGPipeline
        logger.info(f"إنشاء RAG Pipeline: {provider}")
        rag_pipelines[provider] = RAGPipeline(provider=provider)
    return rag_pipelines[provider]


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Endpoint الرئيسي للمحادثة
    يستقبل سؤال ويرجع إجابة
    """
    try:
        logger.info(f"سؤال جديد: {request.message}")

        # جلب أو إنشاء RAG Pipeline
        rag = get_rag_pipeline(request.provider)

        # الحصول على الإجابة
        result = rag.chat(request.message)

        return ChatResponse(
            answer=result["answer"],
            sources=result["sources"],
            success=result["success"],
            provider=request.provider
        )

    except Exception as e:
        logger.error(f"خطأ في الـ API: {e}")
        raise HTTPException(status_code=500, detail=str(e))