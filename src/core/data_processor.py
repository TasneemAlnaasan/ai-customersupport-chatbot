"""
data_processor.py: Data Processor
Uses Pinecone 
"""

import os
from langchain_community.document_loaders import TextLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from src.utils.logger import get_logger
from src.utils.config import settings


logger = get_logger(__name__)


class DataProcessor:

    def __init__(self):
        logger.info("Initializing DataProcessor...")

        # Set Pinecone API Key here
        os.environ["PINECONE_API_KEY"] = settings.pinecone_api_key

        # Gemini Embeddings
        self.embeddings = GoogleGenerativeAIEmbeddings(
            model=settings.gemini_embedding_model,
            google_api_key=settings.gemini_api_key
        )

        # Pinecone Index Name
        self.index_name = "chatbot-index"

        # Text Splitter
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.chunk_size,
            chunk_overlap=settings.chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", ".", " ", ""]
        )

        logger.info("✅ DataProcessor ready!")

    def load_documents(self):
        logger.info(f"Loading files from {settings.raw_data_path}")
        loader = DirectoryLoader(
            settings.raw_data_path,
            glob="**/*.txt",
            loader_cls=TextLoader,
            loader_kwargs={"encoding": "utf-8"}
        )
        documents = loader.load()
        logger.info(f"Loaded {len(documents)} files")
        return documents

    def process(self):
        # 1. Load files
        documents = self.load_documents()
        if not documents:
            logger.warning("No files found!")
            return None

        # 2. Split text
        chunks = self.text_splitter.split_documents(documents)
        logger.info(f"Created {len(chunks)} chunks")

        # 3. Store in Pinecone
        logger.info("Saving to Pinecone...")
        vectorstore = PineconeVectorStore.from_documents(
            documents=chunks,
            embedding=self.embeddings,
            index_name=self.index_name
        )

        logger.info("✅ Saved to Pinecone!")
        return vectorstore

    def load_vectorstore(self):
        logger.info("Loading Pinecone...")
        return PineconeVectorStore(
            index_name=self.index_name,
            embedding=self.embeddings
        )
