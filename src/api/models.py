"""
models.py: شكل البيانات
يحدد ما يدخل ويخرج من الـ API
"""

from pydantic import BaseModel


class ChatRequest(BaseModel):
    """شكل طلب المستخدم"""
    message: str
    provider: str = "groq"  # groq أو gemini

    class Config:
        json_schema_extra = {
            "example": {
                "message": "ما هو سعر TechBot Pro؟",
                "provider": "groq"
            }
        }


class ChatResponse(BaseModel):
    """شكل الإجابة"""
    answer: str
    sources: list
    success: bool
    provider: str