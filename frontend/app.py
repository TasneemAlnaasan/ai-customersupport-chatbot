import streamlit as st
import requests
import time
import threading

# 1. وضع الرابط في البداية لتجنب أخطاء التعريف
API_URL = "https://ai-customersupport-chatbot.onrender.com"

def keep_alive():
    """يصحّي Backend كل 10 دقائق"""
    while True:
        try:
            # تأكد أن الـ Backend لديه مسار باسم / أو /health
            requests.get(f"{API_URL}/", timeout=10)
        except:
            pass
        time.sleep(600)

# شغّل الـ Thread مرة واحدة فقط باستخدام st.cache_resource لمنع تكراره مع كل rerun
@st.cache_resource
def start_keep_alive():
    thread = threading.Thread(target=keep_alive, daemon=True)
    thread.start()
    return True

start_keep_alive()

# ===== إعداد الصفحة =====
st.set_page_config(
    page_title="TechBot Support",
    page_icon="🤖",
    layout="wide"
)

# ... (باقي كود الواجهة كما هو) ...

# عند معالجة السؤال، تأكد من طباعة الخطأ إذا فشل
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    with st.spinner("🤔 جاري التفكير..."):
        try:
            # أضف / في نهاية الرابط إذا كان الـ Backend يتطلب ذلك
            target_url = f"{API_URL}/chat"
            
            response = requests.post(
                target_url,
                json={
                    "message": user_input,
                    "provider": "groq" # القيمة الافتراضية
                },
                timeout=120
            )
            
            if response.status_code == 200:
                data = response.json()
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": data["answer"],
                    "sources": data.get("sources", [])
                })
                st.session_state.total_queries += 1
                st.rerun() # تحديث الصفحة لعرض الرد
            else:
                st.error(f"الخادم استجاب بخطأ {response.status_code}: {response.text}")
        
        except Exception as e:
            st.error(f"فشل الاتصال: {str(e)}")