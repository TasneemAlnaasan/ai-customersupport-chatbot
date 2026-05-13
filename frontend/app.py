import streamlit as st
import requests
import time
import threading

API_URL = "https://ai-customersupport-chatbot.onrender.com"

# منع تكرار الـ Thread
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

# إعدادات الواجهة
st.set_page_config(page_title="TechBot Support", page_icon="🤖")
st.title("🤖 TechBot Customer Support")

if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض المحادثة
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
        if msg["role"] == "assistant" and msg.get("sources"):
            with st.expander("📚 المصادر"):
                for s in msg["sources"]:
                    st.info(f"{s['source']}: {s['content']}")

# مدخلات المستخدم
user_input = st.chat_input("كيف يمكنني مساعدتك اليوم؟")

if user_input:
    # 1. عرض سؤال المستخدم فوراً
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    # 2. طلب الرد من الـ API
    with st.spinner("🤔 جاري التفكير..."):
        try:
            response = requests.post(
                f"{API_URL}/chat",
                json={
                    "message": user_input,
                    "provider": "groq"
                },
                timeout=150 # وقت طويل لأن Render المجاني بطيء في البداية
            )
            
            if response.status_code == 200:
                data = response.json()
                # إضافة رد البوت للذاكرة
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": data["answer"],
                    "sources": data.get("sources", [])
                })
                st.rerun() # لإعادة بناء الواجهة وعرض الرد الجديد
            else:
                st.error(f"خطأ من الخادم ({response.status_code}): {response.text}")
        except Exception as e:
            st.error(f"حدث خطأ في الاتصال: {e}")