
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # LLM Providers
    groq_api_key: str = ""
    gemini_api_key: str = ""

    # Virtual model for each provider
    groq_model: str = "llama-3.1-8b-instant"
    gemini_model: str = "gemini-2.0-flash"

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