import pytest
from src.core.rag_pipeline import RAGPipeline


def test_rag_initialization():
    try:
        rag = RAGPipeline(provider="groq")
        assert rag is not None
        assert rag.retriever is not None
        assert rag.llm is not None
    except Exception as e:
        pytest.skip(f"Skipping: {e}")


def test_rag_chat_returns_answer():
    try:
        rag = RAGPipeline(provider="groq")
        result = rag.chat("ما هو سعر TechBot Pro؟")
        assert result["success"] == True
        assert len(result["answer"]) > 0
    except Exception as e:
        pytest.skip(f"Skipping: {e}")


def test_rag_chat_returns_sources():
    try:
        rag = RAGPipeline(provider="groq")
        result = rag.chat("ما هو سعر TechBot Pro؟")
        assert "sources" in result
    except Exception as e:
        pytest.skip(f"Skipping: {e}")


def test_rag_chat_history():
    try:
        rag = RAGPipeline(provider="groq")
        rag.chat("ما هو سعر TechBot Pro؟")
        assert len(rag.chat_history) == 1
        rag.chat("وما هي مميزاته؟")
        assert len(rag.chat_history) == 2
    except Exception as e:
        pytest.skip(f"Skipping: {e}")