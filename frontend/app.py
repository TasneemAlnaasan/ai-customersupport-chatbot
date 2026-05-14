import streamlit as st
import requests
import time
import threading

st.set_page_config(
    page_title="TechBot Customer Support",
    page_icon="🤖",
    layout="wide"
)

API_URL = "https://ai-customersupport-chatbot.onrender.com"

@st.cache_resource
def start_keep_alive():
    def keep_alive():
        while True:
            try:
                requests.get(f"{API_URL}/", timeout=5)
            except:
                pass
            time.sleep(600)
    thread = threading.Thread(target=keep_alive, daemon=True)
    thread.start()
    return True

start_keep_alive()

# ===== Header =====
st.title("🤖 TechBot Customer Support")
st.caption("مرحباً! أنا مساعدك الذكي. كيف يمكنني مساعدتك؟")
st.divider()

# ===== Layout =====
col1, col2 = st.columns([3, 1])

# ===== Session State =====
if "messages" not in st.session_state:
    st.session_state.messages = []
if "total_queries" not in st.session_state:
    st.session_state.total_queries = 0

with col2:
    st.metric("عدد الأسئلة", st.session_state.total_queries)
    st.divider()
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

with col1:
    # عرض المحادثة
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if msg["role"] == "assistant" and msg.get("sources"):
                with st.expander("📚 المصادر"):
                    for s in msg["sources"]:
                        st.info(f"📄 {s.get('source', 'Unknown')}\n\n{s.get('content', '')}")

# ===== معالجة السؤال =====
user_input = st.chat_input("كيف يمكنني مساعدتك اليوم؟")

if "pending" in st.session_state:
    user_input = st.session_state.pending
    del st.session_state.pending

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.spinner("🤔 جاري التفكير..."):
        try:
            response = requests.post(
                f"{API_URL}/chat",
                json={"message": user_input, "provider": "groq"},
                timeout=120
            )

            if response.status_code == 200:
                data = response.json()
                answer = data.get("answer", "عذراً، لم أستطع إيجاد إجابة.")
                sources = data.get("sources", [])

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer,
                    "sources": sources
                })
                st.session_state.total_queries += 1

            else:
                st.error(f"خطأ {response.status_code}: {response.text}")

        except requests.exceptions.Timeout:
            st.error("❌ انتهى وقت الانتظار.")
        except Exception as e:
            st.error(f"❌ حدث خطأ: {e}")

    st.rerun()