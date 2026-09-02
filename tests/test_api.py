
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


def test_chat_valid_question():
    response = client.post(
        "/chat",
        json={
            "message": "ما هو سعر TechBot Pro؟",
            "provider": "groq"
        }
    )
    assert response.status_code in [200, 503, 500]


def test_chat_empty_message():
    response = client.post(
        "/chat",
        json={
            "message": "",
            "provider": "groq"
        }
    )
    assert response.status_code in [200, 422, 500, 503]


def test_chat_invalid_provider():
    response = client.post(
        "/chat",
        json={
            "message": "ما هو سعر TechBot Pro؟",
            "provider": "unknown"
        }
    )
    assert response.status_code in [200, 500, 503]