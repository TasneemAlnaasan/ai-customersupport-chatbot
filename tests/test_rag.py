"""
test_rag.py: اختبار الـ RAG Pipeline
"""

from src.core.rag_pipeline import RAGPipeline


def test_rag_initialization():
    """تحقق أن RAG Pipeline ينشأ بدون أخطاء"""
    rag = RAGPipeline(provider="groq")
    assert rag is not None
    assert rag.retriever is not None
    assert rag.llm is not None


def test_rag_chat_returns_answer():
    """تحقق أن الـ RAG يرجع إجابة"""
    rag = RAGPipeline(provider="groq")
    result = rag.chat("ما هو سعر TechBot Pro؟")
    assert result["success"] == True
    assert len(result["answer"]) > 0


def test_rag_chat_returns_sources():
    """تحقق أن الـ RAG يرجع مصادر"""
    rag = RAGPipeline(provider="groq")
    result = rag.chat("ما هو سعر TechBot Pro؟")
    assert "sources" in result
    assert len(result["sources"]) > 0


def test_rag_chat_history():
    """تحقق أن الـ RAG يتذكر المحادثة"""
    rag = RAGPipeline(provider="groq")
    
    # سؤال أول
    rag.chat("ما هو سعر TechBot Pro؟")
    
    # تحقق أن التاريخ اتحفظ
    assert len(rag.chat_history) == 1
    
    # سؤال ثاني
    rag.chat("وما هي مميزاته؟")
    assert len(rag.chat_history) == 2