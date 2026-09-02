
from langchain_community.document_loaders import TextLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from src.utils.logger import get_logger
from src.utils.config import settings
from pinecone import Pinecone


logger = get_logger(__name__)


class DataProcessor:

    def __init__(self):
        logger.info("تهيئة DataProcessor...")

        # Gemini Embeddings
        self.embeddings = GoogleGenerativeAIEmbeddings(
            model="models/gemini-embedding-001",
            google_api_key=settings.gemini_api_key
        )

        # Pinecone Client
        self.pc = Pinecone(api_key=settings.pinecone_api_key)
        self.index_name = "chatbot-index"

        # Text Splitter
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.chunk_size,
            chunk_overlap=settings.chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", ".", " ", ""]
        )

        logger.info("✅ DataProcessor جاهز!")

    def load_documents(self):
        logger.info(f"تحميل الملفات من {settings.raw_data_path}")
        loader = DirectoryLoader(
            settings.raw_data_path,
            glob="**/*.txt",
            loader_cls=TextLoader,
            loader_kwargs={"encoding": "utf-8"}
        )
        documents = loader.load()
        logger.info(f"تم تحميل {len(documents)} ملف")
        return documents

    def process(self):
        # 1. Files Loading
        documents = self.load_documents()
        if not documents:
            logger.warning("لا توجد ملفات!")
            return None

        # 2.  Text splitting
        chunks = self.text_splitter.split_documents(documents)
        logger.info(f"تم إنشاء {len(chunks)} chunk")

        # 3. Store in Pinecone
        logger.info("حفظ في Pinecone...")
        import os
        os.environ["PINECONE_API_KEY"] = settings.pinecone_api_key
        vectorstore = PineconeVectorStore.from_documents(
                documents=chunks,
                embedding=self.embeddings,
                index_name=self.index_name
        )

        logger.info("✅ تم الحفظ في Pinecone!")
        return vectorstore

    def load_vectorstore(self):
        import os
        os.environ["PINECONE_API_KEY"] = settings.pinecone_api_key
        logger.info("تحميل Pinecone...")
        return PineconeVectorStore(
            index_name=self.index_name,
            embedding=self.embeddings
        )