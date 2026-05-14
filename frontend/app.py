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


# تهيئة الذاكرة
if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض المحادثة (هذا الجزء هو الذي يعرض الردود بعد الـ rerun)
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"]) # استخدام markdown أفضل للعرض
        if msg["role"] == "assistant" and msg.get("sources"):
            with st.expander("📚 المصادر"):
                for s in msg["sources"]:
                    st.info(f"📄 {s.get('source', 'Unknown')}\n\n{s.get('content', '')}")

# مدخلات المستخدم
user_input = st.chat_input("كيف يمكنني مساعدتك اليوم؟")

if user_input:
    # إضافة سؤال المستخدم وعرضه فوراً
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.spinner("🤔 جاري التفكير..."):
        try:
            # الطلب إلى الـ API
            response = requests.post(
                f"{API_URL}/chat",
                json={
                    "message": user_input,
                    "provider": "groq"
                },
                timeout=120
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # التحقق من وجود الإجابة
                answer = data.get("answer", "عذراً، لم أستطع إيجاد إجابة.")
                sources = data.get("sources", [])
                
                # إضافة الرد للذاكرة
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer,
                    "sources": sources
                })
                
                # تحديث الصفحة لعرض الرد الجديد من الـ session_state
                st.rerun() 
            else:
                st.error(f"خطأ {response.status_code}: {response.text}")
        except requests.exceptions.Timeout:
            st.error("❌ انتهى وقت الانتظار. السيرفر مستغرق في التفكير أو في وضع السكون.")
        except Exception as e:
            st.error(f"❌ حدث خطأ: {e}")