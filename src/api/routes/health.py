"""
health.py: التحقق أن الـ API يعمل
"""

from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
async def health_check():
    """
    يستخدمه الـ Monitoring للتحقق
    أن السيرفر يعمل بشكل صحيح
    """
    return {
        "status": "healthy",
        "message": "API يعمل بشكل صحيح ✅"
    }