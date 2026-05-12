
from langchain_community.document_loaders import TextLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from src.utils.logger import get_logger
from src.utils.config import settings
import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings

logger = get_logger(__name__)


class DataProcessor:
    def __init__(self):
        logger.info("Loading Embeddings Model...")
        self.embeddings = GoogleGenerativeAIEmbeddings(
            model="models/gemini-embedding-001",
            google_api_key=settings.gemini_api_key
        )

        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.chunk_size,  
            chunk_overlap=settings.chunk_overlap, 
            length_function=len,
            separators=["\n\n", "\n", ".", " ", ""]
        )

        logger.info("DataProcessor Ready ")

    def load_documents(self):
        logger.info(f"Loading files from {settings.raw_data_path}")

        loader = DirectoryLoader(
            settings.raw_data_path,
            glob="**/*.txt", 
            loader_cls=TextLoader,
            loader_kwargs={"encoding": "utf-8"}
        )

        documents = loader.load()
        logger.info(f"{len(documents)} Foles were uploaded")
        return documents

    def process(self):
        documents = self.load_documents()

        if not documents:
            logger.warning("No files in data/raw!")
            return None

        # 2. تقسيم النص لـ chunks
        chunks = self.text_splitter.split_documents(documents)
        logger.info(f"{len(chunks)} chunks were created")

        logger.info(" Saved in ChromaDB...")
        vectorstore = Chroma.from_documents(
            documents=chunks,
            embedding=self.embeddings,
            persist_directory=settings.vectorstore_path
        )

        logger.info(f"✅ {len(chunks)} chunks were saved in ChromaDB")
        return vectorstore

    def load_vectorstore(self):
        if not os.path.exists(settings.vectorstore_path):
            logger.warning("ChromaDB غير موجودة! شغّل process() أولاً")
            return None

        logger.info("Loading ChromaDB ...")
        return Chroma(
            persist_directory=settings.vectorstore_path,
            embedding_function=self.embeddings
        )