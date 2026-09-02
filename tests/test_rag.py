
from src.core.rag_pipeline import RAGPipeline


def test_rag_initialization():
    rag = RAGPipeline(provider="groq")
    assert rag is not None
    assert rag.retriever is not None
    assert rag.llm is not None


def test_rag_chat_returns_answer():
    rag = RAGPipeline(provider="groq")
    result = rag.chat("ما هو سعر TechBot Pro؟")
    assert result["success"] == True
    assert len(result["answer"]) > 0


def test_rag_chat_returns_sources():
    rag = RAGPipeline(provider="groq")
    result = rag.chat("ما هو سعر TechBot Pro؟")
    assert "sources" in result
    assert len(result["sources"]) > 0


def test_rag_chat_history():
    rag = RAGPipeline(provider="groq")
    
    rag.chat("ما هو سعر TechBot Pro؟")
    
    assert len(rag.chat_history) == 1
   
    rag.chat("وما هي مميزاته؟")
    assert len(rag.chat_history) == 2