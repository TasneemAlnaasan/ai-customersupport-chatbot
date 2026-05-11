"""
main.py: نقطة البداية للـ API
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.routes import chat, health
from src.utils.logger import setup_logger, get_logger
import os 
from src.utils.config import settings

# إعداد الـ Logger
setup_logger()
logger = get_logger(__name__)

# إنشاء التطبيق
app = FastAPI(
    title="AI Customer Support Chatbot",
    description="Chatbot مدعوم بـ RAG",
    version="1.0.0"
)

# CORS: يسمح للـ Frontend بالتواصل مع الـ API
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
    return {"message": "🤖 AI Chatbot API يعمل!"}



# تفعيل LangSmith Monitoring
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = settings.langsmith_api_key
os.environ["LANGCHAIN_PROJECT"] = settings.langsmith_project