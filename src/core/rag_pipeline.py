"""
rag_pipeline.py: القلب الحقيقي للـ Chatbot
يستخدم Pinecone بدل ChromaDB
"""

from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from src.core.data_processor import DataProcessor
from src.core.llm_handler import LLMHandler
from src.utils.logger import get_logger
from src.utils.config import settings

logger = get_logger(__name__)


PROMPT_TEMPLATE = """You are a helpful customer support assistant for TechBot Solutions.
Answer questions based ONLY on the context provided.
If you don't know, say: please contact support@techbot.com
Answer in the same language the user uses.

Context:
{context}

Chat History:
{chat_history}

Question: {question}

Answer:"""


class RAGPipeline:

    def __init__(self, provider: str = "groq"):
        self.provider = provider
        self.retriever = None
        self.llm = None
        self.chat_history = []
        self._setup()

    def _setup(self):
        # 1. تحميل Pinecone
        logger.info("تحميل Pinecone...")
        processor = DataProcessor()
        vectorstore = processor.load_vectorstore()

        if not vectorstore:
            raise Exception("Pinecone غير موجود!")

        # 2. Retriever
        self.retriever = vectorstore.as_retriever(
            search_type="similarity",
            search_kwargs={"k": settings.retriever_k}
        )

        # 3. تحميل LLM
        logger.info(f"تحميل LLM: {self.provider}")
        llm_handler = LLMHandler()
        self.llm = llm_handler.get_llm(self.provider)

        logger.info("✅ RAG Pipeline جاهز!")

    def _format_docs(self, docs):
        return "\n\n".join(doc.page_content for doc in docs)

    def _format_history(self):
        if not self.chat_history:
            return ""
        history_text = ""
        for question, answer in self.chat_history:
            history_text += f"User: {question}\nAssistant: {answer}\n\n"
        return history_text

    def chat(self, question: str) -> dict:
        try:
            logger.info(f"سؤال: {question}")

            # 1. البحث في Pinecone
            docs = self.retriever.invoke(question)
            context = self._format_docs(docs)
            history = self._format_history()

            # 2. بناء الـ Prompt
            prompt_template = PromptTemplate(
                input_variables=["context", "chat_history", "question"],
                template=PROMPT_TEMPLATE
            )

            # 3. إرسال للـ LLM
            chain = prompt_template | self.llm | StrOutputParser()
            answer = chain.invoke({
                "context": context,
                "chat_history": history,
                "question": question
            })

            # 4. حفظ في التاريخ
            self.chat_history.append((question, answer))
            if len(self.chat_history) > 5:
                self.chat_history = self.chat_history[-5:]

            # 5. استخراج المصادر
            sources = []
            for doc in docs:
                sources.append({
                    "content": doc.page_content[:200],
                    "source": doc.metadata.get("source", "غير معروف")
                })

            logger.info(f"إجابة: {answer[:100]}...")

            return {
                "answer": answer,
                "sources": sources,
                "success": True
            }

        except Exception as e:
            logger.error(f"خطأ: {e}")
            return {
                "answer": "عذراً، حدث خطأ. يرجى المحاولة مرة أخرى.",
                "sources": [],
                "success": False,
                "error": str(e)
            }
