"""
app.py: واجهة المستخدم
مبنية بـ Streamlit فقط بدون CSS
"""

import streamlit as st
import requests
import time

# ===== إعداد الصفحة =====
st.set_page_config(
    page_title="TechBot Support",
    page_icon="🤖",
    layout="wide"
)

# ===== Header =====
st.title("🤖 TechBot Customer Support")
st.caption("مرحباً! أنا مساعدك الذكي. كيف يمكنني مساعدتك؟")
st.divider()

# ===== Session State =====
if "messages" not in st.session_state:
    st.session_state.messages = []
if "total_queries" not in st.session_state:
    st.session_state.total_queries = 0

# ===== Layout =====
col1, col2 = st.columns([3, 1])

with col1:
    # عرض تاريخ المحادثة
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

            # عرض المصادر
            if message["role"] == "assistant" and message.get("sources"):
                with st.expander("📚 المصادر"):
                    for source in message["sources"]:
                        st.info(f"📄 {source['source']}\n\n{source['content']}")

with col2:
    # إحصاءات
    st.metric("عدد الأسئلة", st.session_state.total_queries)
    st.divider()

    # اختيار المزود
    provider = st.selectbox(
        "🤖 اختر الـ AI",
        ["groq", "gemini"],
        index=0
    )
    st.divider()

    # أسئلة مقترحة
    st.markdown("💡 **أسئلة مقترحة**")
    questions = [
        "ما هو سعر TechBot Pro؟",
        "هل يدعم اللغة العربية؟",
        "ما هي سياسة الاسترداد؟",
        "كيف أتواصل مع الدعم؟"
    ]

    for q in questions:
        if st.button(q, use_container_width=True):
            st.session_state.pending = q

# ===== معالجة السؤال =====
API_URL = "https://ai-customersupport-chatbot.onrender.com"

user_input = st.chat_input("اكتب سؤالك هنا...")

if "pending" in st.session_state:
    user_input = st.session_state.pending
    del st.session_state.pending

if user_input:
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.spinner("🤔 جاري التفكير..."):
        try:
            start = time.time()
            response = requests.post(
                f"{API_URL}/chat",
                json={
                    "message": user_input,
                    "provider": provider
                },
                timeout=30
            )
            elapsed = time.time() - start

            if response.status_code == 200:
                data = response.json()

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": data["answer"],
                    "sources": data["sources"]
                })

                st.session_state.total_queries += 1
                st.toast(f"✅ إجابة في {elapsed:.1f} ثانية")

            else:
                st.error("حدث خطأ في الـ API")

        except requests.exceptions.ConnectionError:
            st.error("❌ تأكد أن الـ API يعمل على Port 8000")

    st.rerun()