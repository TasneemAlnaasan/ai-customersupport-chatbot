"""
test_api.py: اختبار الـ API
"""

from fastapi.testclient import TestClient
from src.api.main import app

# TestClient يختبر الـ API بدون تشغيله
client = TestClient(app)


def test_root():
    """تحقق أن الـ API يرد"""
    response = client.get("/")
    assert response.status_code == 200


def test_health_check():
    """تحقق أن الـ API صحي"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


def test_chat_valid_question():
    """تحقق أن الـ Chatbot يجيب"""
    response = client.post(
        "/chat",
        json={
            "message": "ما هو سعر TechBot Pro؟",
            "provider": "groq"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] == True
    assert len(data["answer"]) > 0


def test_chat_empty_message():
    """تحقق من السؤال الفارغ"""
    response = client.post(
        "/chat",
        json={
            "message": "",
            "provider": "groq"
        }
    )
    # يجب أن يرد بشكل ما
    assert response.status_code in [200, 422]


def test_chat_invalid_provider():
    """تحقق من مزود غير موجود"""
    response = client.post(
        "/chat",
        json={
            "message": "ما هو سعر TechBot Pro؟",
            "provider": "unknown"
        }
    )
    # يجب أن يستخدم groq افتراضياً
    assert response.status_code == 200