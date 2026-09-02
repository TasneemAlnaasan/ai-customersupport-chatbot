
from pydantic import BaseModel


class ChatRequest(BaseModel):
    message: str
    provider: str = "groq"  

    class Config:
        json_schema_extra = {
            "example": {
                "message": "ما هو سعر TechBot Pro؟",
                "provider": "groq"
            }
        }


class ChatResponse(BaseModel):
    answer: str
    sources: list
    success: bool
    provider: str