"""
chat.py: مسار المحادثة الرئيسي
"""

from fastapi import APIRouter, HTTPException
from src.api.models import ChatRequest, ChatResponse
from src.utils.logger import get_logger

logger = get_logger(__name__)
router = APIRouter()


def get_rag_pipeline(provider: str):
    from src.api.main import rag_instance
    if rag_instance:
        return rag_instance
    from src.core.rag_pipeline import RAGPipeline
    return RAGPipeline(provider=provider)


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        logger.info(f"سؤال جديد: {request.message}")
        rag = get_rag_pipeline(request.provider)
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