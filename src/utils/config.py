
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # LLM Provider
    groq_api_key: str = ""
    gemini_api_key: str =""
    pinecone_api_key: str=""
    

    # Virtual model for the provider
    groq_model: str = "llama-3.1-8b-instant"
    

    # Langsmith Monitoring
    langsmith_api_key: str = ""
    langsmith_project: str = "ai-chatbot"
    langsmith_tracing: bool = True

    # App Settings
    app_env: str = "development"
    log_level: str = "INFO"

    # RAG Settings
    vectorstore_path: str = "./data/vectorstore"
    raw_data_path: str = "./data/raw"
    chunk_size: int = 1000
    chunk_overlap: int = 200
    retriever_k: int = 3

    # LLM Generation
    temperature: float = 0.1
    max_tokens: int = 1024

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"



@lru_cache()
def get_settings() -> Settings:
    return Settings()

settings = get_settings()