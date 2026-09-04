---
title: AI Customer Support Chatbot
emoji: 🤖
colorFrom: blue
colorTo: purple
sdk: streamlit
sdk_version: "1.38.0"
python_version: "3.11"
app_file: frontend/app.py
pinned: false
---


> Intelligent chatbot powered by RAG (Retrieval Augmented Generation)
> built for customer support automation.



![Python](https://img.shields.io/badge/Python-3.11-blue)




![FastAPI](https://img.shields.io/badge/FastAPI-latest-green)




![LangChain](https://img.shields.io/badge/LangChain-latest-orange)




![Streamlit](https://img.shields.io/badge/Streamlit-1.38-red)



---

## 🌐 Live Demo

- **Frontend:** https://ai-customersupport-chatbot-frontend.onrender.com 
- **Backend API:** https://ai-customersupport-chatbot.onrender.com/docs

---

## 🏗️ System Architecture

```

User → Frontend (Streamlit on Hugging Face)
              ↓
       Backend API (FastAPI on Render)
              ↓
         RAG Pipeline
          ↙        ↘
    Pinecone        Groq LLM
   (Vector DB)    (LLaMA 3.1)
        ↑
   Gemini Embeddings
```

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| LLM | Groq (LLaMA 3.1-8b) |
| Embeddings | Google Gemini |
| RAG Framework | LangChain |
| Vector Database | Pinecone |
| Backend API | FastAPI |
| Frontend | Streamlit |
| Monitoring | LangSmith |
| CI/CD | GitHub Actions |
| Backend Hosting | Render |
| Frontend Hosting | Hugging Face Spaces |

---

## 📁 Project Structure

```
ai-customer-support-chatbot/
├── src/
│   ├── api/
│   │   ├── main.py           # FastAPI app
│   │   ├── models.py         # Pydantic models
│   │   └── routes/
│   │       ├── chat.py       # Chat endpoints
│   │       └── health.py     # Health check
│   ├── core/
│   │   ├── rag_pipeline.py   # RAG logic
│   │   ├── llm_handler.py    # LLM integration
│   │   └── data_processor.py # Data processing
│   └── utils/
│       ├── config.py         # Configuration
│       └── logger.py         # Logging
├── frontend/
│   └── app.py                # Streamlit UI
├── data/
│   └── raw/                  # Company documents
├── tests/
│   ├── test_api.py
│   └── test_rag.py
├── .github/workflows/
│   └── ci-cd.yml             # GitHub Actions
└── render.yaml               # Deployment config

```

---

## 🔄 How It Works

```
1. المستخدم يسأل سؤال
2. السؤال يتحول لـ vector (Gemini Embeddings)
3. البحث في Pinecone عن أقرب chunks
4. إرسال السؤال + السياق لـ Groq LLM
5. الإجابة ترجع للمستخدم
```

---

## 🚀 Quick Start

### 1. Clone the repository
```bash
git clone https://github.com/TasneemAlnaasan/ai-customersupport-chatbot
cd ai-customersupport-chatbot
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Setup environment variables
```bash
cp .env.example .env
# Add your API keys in .env
```

### 4. Process documents
```bash
python -c "from src.core.data_processor import DataProcessor; dp = DataProcessor(); dp.process()"
```

### 5. Start the API
```bash
uvicorn src.api.main:app --reload --port 8000
```

### 6. Start the Frontend
```bash
streamlit run frontend/app.py --server.port 8501
```

---

## 🔑 Environment Variables

```env
GROQ_API_KEY=your_groq_key
GEMINI_API_KEY=your_gemini_key
PINECONE_API_KEY=your_pinecone_key
LANGSMITH_API_KEY=your_langsmith_key
LANGSMITH_PROJECT=ai-chatbot
```

---

## ✨ Key Features

- ✅ RAG-based responses with source citations
- ✅ Conversation memory (last 5 messages)
- ✅ Multi-language support (Arabic/English)
- ✅ Production monitoring with LangSmith
- ✅ CI/CD with GitHub Actions
- ✅ Cloud deployment (Render + Hugging Face)
- ✅ Keep Alive mechanism for backend

---

## 🧪 Running Tests

```bash
pytest tests/ -v
```

---

## 📊 Monitoring

```
LangSmith tracks:
- Every question and answer
- Response times
- Token usage
- Errors in production
```

---

## 🎯 What I Learned

- Designing RAG pipelines from scratch
- Building production-grade FastAPI applications
- Vector databases and semantic search
- LLM prompt engineering
- Cloud deployment and CI/CD
- Debugging production issues
- Git branching strategies

---

## 👨‍💻 Author

**Tasneem AlNaasan**
- GitHub: [@TasneemAlnaasan](https://github.com/TasneemAlnaasan)
- LinkedIn: 
```