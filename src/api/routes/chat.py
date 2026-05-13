from fastapi import APIRouter, HTTPException, Request # أضف Request
from src.api.models import ChatRequest, ChatResponse
from src.utils.logger import get_logger

logger = get_logger(__name__)
router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest, fastapi_req: Request): # أضف fastapi_req هنا
    try:
        logger.info(f"سؤال جديد: {request.message}")
        
        # الوصول للـ Pipeline المخزن في الـ App State
        rag = getattr(fastapi_req.app.state, "rag_pipeline", None)
        
        if not rag:
            logger.error("RAG Pipeline غير محمل في الـ State")
            raise HTTPException(status_code=503, detail="Pipeline is still loading...")

        # تنفيذ المحادثة
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