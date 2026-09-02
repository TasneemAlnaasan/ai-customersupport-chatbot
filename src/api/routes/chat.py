from fastapi import APIRouter, HTTPException, Request 
from src.api.models import ChatRequest, ChatResponse
from src.utils.logger import get_logger

logger = get_logger(__name__)
router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest, fastapi_req: Request): 
    try:
        logger.info(f"سؤال جديد: {request.message}")
        rag = getattr(fastapi_req.app.state, "rag_pipeline", None)
        
        if not rag:
            logger.error("RAG Pipeline غير محمل في الـ State")
            raise HTTPException(status_code=503, detail="Pipeline is still loading...")

        
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