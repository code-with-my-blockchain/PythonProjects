import streamlit as st
import requests

BASE_URL = "http://127.0.0.1:8000/api/v1"

st.set_page_config(
    page_title="Enterprise AI Knowledge Assistant",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Enterprise AI Knowledge Assistant")
st.caption("Powered by RAG & FastAPI Backend Engine")

if "token" not in st.session_state:
    st.session_state.token = None
if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.header("🔑 Authentication")
    
    if not st.session_state.token:
        username = st.text_input("Username", value="admin")
        password = st.text_input("Password", type="password")
        
        if st.button("Login"):
            try:
                response = requests.post(
                    f"{BASE_URL}/auth/login",
                    data={"username": username, "password": password},
                    proxies={"http": None, "https": None}
                )
                if response.status_code == 200:
                    st.session_state.token = response.json().get("access_token")
                    st.success("Successfully logged in!")
                    st.rerun()
                else:
                    st.error("Invalid credentials")
            except Exception as e:
                st.error(f"Cannot connect to backend: {e}")
    else:
        st.success("Status: Authenticated 🔒")
        if st.button("Logout"):
            st.session_state.token = None
            st.session_state.messages = []
            st.rerun()

    st.markdown("---")
    st.header("📄 Knowledge Base")
    
    # Document Upload Section
    uploaded_file = st.file_uploader("Upload PDF / Text Document", type=["pdf", "txt"])
    if uploaded_file and st.button("Upload & Index"):
        if st.session_state.token:
            headers = {"Authorization": f"Bearer {st.session_state.token}"}
            files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
            
            with st.spinner("Processing document..."):
                try:
                    res = requests.post(f"{BASE_URL}/documents/upload", headers=headers, files=files)
                    if res.status_code == 200:
                        st.success("Document uploaded & indexed!")
                    else:
                        st.error(f"Upload failed: {res.text}")
                except Exception as e:
                    st.error(f"Error: {e}")
        else:
            st.warning("Please login first to upload documents.")

if not st.session_state.token:
    st.info("👈 Please login from the sidebar to start chatting with the Knowledge Assistant.")
else:
   
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

  
    if prompt := st.chat_input("Ask anything about your uploaded documents..."):
       
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

    
        headers = {"Authorization": f"Bearer {st.session_state.token}"}
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    res = requests.post(
                        f"{BASE_URL}/chat/query",
                        headers=headers,
                        json={"query": prompt}
                    )
                    if res.status_code == 200:
                        bot_response = res.json().get("response", "No response received.")
                    else:
                        bot_response = f"Error: {res.status_code} - {res.text}"
                except Exception as e:
                    bot_response = f"Failed to connect to AI Engine: {e}"

                st.markdown(bot_response)
                st.session_state.messages.append({"role": "assistant", "content": bot_response})