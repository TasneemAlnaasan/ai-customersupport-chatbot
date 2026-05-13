"""
main.py: نقطة البداية للـ API
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.routes import chat, health
from src.utils.logger import setup_logger, get_logger
import os 
from src.utils.config import settings
from contextlib import asynccontextmanager
from src.core.rag_pipeline import RAGPipeline

# إعداد الـ Logger
setup_logger()
logger = get_logger(__name__)

# تفعيل LangSmith
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = settings.langsmith_api_key
os.environ["LANGCHAIN_PROJECT"] = settings.langsmith_project

# RAG Pipeline العام
rag_instance = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    # عند بدء التشغيل
    logger.info("تحميل RAG Pipeline...")
    # إنشاء الـ instance وتخزينه في الـ state
    app.state.rag_pipeline = RAGPipeline(provider="groq")
    logger.info("✅ RAG Pipeline جاهز في الـ State!")
    yield
    # عند الإيقاف
    logger.info("إيقاف التطبيق...")

# إنشاء التطبيق
app = FastAPI(
    title="AI Customer Support Chatbot",
    description="Chatbot مدعوم بـ RAG",
    version="1.0.0",
    lifespan=lifespan
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# تسجيل الـ Routes
app.include_router(health.router)
app.include_router(chat.router)
@app.get("/")
async def root():
    return {"message": "AI Chtbot API يعمل"}

@app.get("/")
async def health_check():
    return {"status": "online"}
    
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = settings.langsmith_api_key
os.environ["LANGCHAIN_PROJECT"] = settings.langsmith_project