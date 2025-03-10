import os
import requests
import streamlit as st

# Set page config
st.set_page_config(
    page_title="EthosEdge (Free Chatbot)",
    page_icon="🤖",
    layout="wide"
)

# Initialize session state variables
if "chat_sessions" not in st.session_state:
    st.session_state.chat_sessions = {}
if "current_chat" not in st.session_state:
    st.session_state.current_chat = None
if "chats" not in st.session_state:
    st.session_state.chats = []

# Centered title with warm, supportive messaging
st.markdown("""
    <h1 style="text-align: center;">EthosEdge (Your Supportive Chatbot)</h1>
    <h3 style="text-align: center; color: #4CAF50;"> We're Here for You 💙</h3>
""", unsafe_allow_html=True)

# Sidebar for chat management
with st.sidebar:
    st.header("Chat Management")
    chat_name_input = st.text_input("Enter chat name:")
    if st.button("Start New Chat"):
        if chat_name_input:
            st.session_state.current_chat = chat_name_input
            st.session_state.chat_sessions[chat_name_input] = []
            st.session_state.chats = []
        else:
            st.warning("Please enter a chat name before starting a new chat.")
    
    st.markdown("---")
    st.header("Chat History")
    for chat_name in st.session_state.chat_sessions.keys():
        if st.button(chat_name, key=chat_name):
            st.session_state.current_chat = chat_name
            st.session_state.chats = st.session_state.chat_sessions[chat_name]
            st.rerun()

# Chat Interface using Together AI (Free API)
TOGETHER_API_URL = "https://api.together.xyz/v1/chat/completions"
HEADERS = {"Authorization": "Bearer 7d86fd8a0981c8e37642cfdc13da0439edb2d76de30a14ae793a84674e74814b", "Content-Type": "application/json"}

def query_together(messages):
    system_message = {"role": "system", "content": "You are a kind, supportive, and empathetic office assistant who always reassures users and makes them feel heard and valued."}
    payload = {
        "model": "mistralai/Mistral-7B-Instruct-v0.1",
        "messages": [system_message] + messages,
        "max_tokens": 200
    }
    response = requests.post(TOGETHER_API_URL, headers=HEADERS, json=payload)
    if response.status_code == 200:
        return response.json().get("choices", [{}])[0].get("message", {}).get("content", "I'm here for you. Please feel free to share what's on your mind. 💙").strip()
    return "I'm always here to listen. If you're struggling, please don't hesitate to reach out. 💙"

if st.session_state.current_chat:
    for chat in st.session_state.chats:
        if chat['role'] == "user":
            st.chat_message("user").markdown(f"**You:** {chat['content']}")
        else:
            st.chat_message("assistant").markdown(f"**EthosEdge:** {chat['content']}")
    
    prompt = st.chat_input("Type your thoughts, I'm here to listen...")
    if prompt:
        st.session_state.chats.append({"role": "user", "content": prompt})
        response_text = query_together(st.session_state.chats)
        st.session_state.chats.append({"role": "assistant", "content": response_text})
        st.session_state.chat_sessions[st.session_state.current_chat] = list(st.session_state.chats)
        st.rerun()
else:
    with st.container():
        st.markdown(
            """
            <div style='text-align: center; background-color: #082242; padding: 10px; border-radius: 5px;'>
                <p style='margin: 0; font-size: 16px; color: ##a6c1e3;'>
                    Start a new chat or select an existing one from the history. Remember, we're here for you.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )
