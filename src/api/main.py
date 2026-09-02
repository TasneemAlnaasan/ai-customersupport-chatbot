

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from src.api.routes import chat, health
from src.utils.logger import setup_logger, get_logger
from src.utils.config import settings
from src.core.rag_pipeline import RAGPipeline
import os

setup_logger()
logger = get_logger(__name__)

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = settings.langsmith_api_key
os.environ["LANGCHAIN_PROJECT"] = settings.langsmith_project

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("تحميل RAG Pipeline...")
    app.state.rag_pipeline = RAGPipeline(provider="groq")
    logger.info("✅ RAG Pipeline جاهز!")
    yield
    logger.info("إيقاف التطبيق...")

app = FastAPI(
    title="AI Customer Support Chatbot",
    description="Chatbot مدعوم بـ RAG",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(chat.router)

@app.get("/")
async def root():
    return {"status": "online", "message": "🤖 AI Chatbot API يعمل!"}