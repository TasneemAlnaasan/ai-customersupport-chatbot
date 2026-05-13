# Python 3.11 بالضبط
FROM python:3.11-slim

# مجلد العمل
WORKDIR /app

# نسخ المتطلبات أولاً
COPY requirements.txt .

# تثبيت المكتبات
RUN pip install --no-cache-dir -r requirements.txt

# نسخ كل الكود
COPY . .

# بناء ChromaDB عند البناء
RUN python -c "from src.core.data_processor import DataProcessor; dp = DataProcessor(); dp.process()"

# تشغيل التطبيق
CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "10000"]