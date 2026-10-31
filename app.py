import streamlit as st

from config import APP_NAME
from ai_engine import get_ai_response
from database import (
    create_database,
    save_message,
    get_chat_history
)

# Page configuration
st.set_page_config(
    page_title=APP_NAME,
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom professional styling
st.markdown("""
<style>
    .stApp {
        background-color: #0B0F19;
        color: #FFFFFF;
    }

    section[data-testid="stSidebar"] {
        background-color: #111827;
    }

    .main-title {
        font-size: 42px;
        font-weight: 800;
        color: #A78BFA;
        text-align: center;
    }

    .subtitle {
        color: #9CA3AF;
        text-align: center;
        font-size: 17px;
    }

    .stChatMessage {
        border-radius: 14px;
    }

    div[data-testid="stChatInput"] {
        border-radius: 15px;
    }
</style>
""", unsafe_allow_html=True)


# Initialize database
create_database()


# Sidebar
with st.sidebar:

    st.title("🤖 NOVA AI")

    st.caption("Your Intelligent AI Companion")

    st.divider()

    if st.button("＋ New Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.subheader("Features")

    st.markdown("""
    - 💬 AI Conversation
    - 🐍 Python Assistant
    - 🧠 AI & ML Tutor
    - 📚 Student Mode
    """)

    st.divider()

    st.caption("NOVA AI | Version 1.0")


# Initialize chat session
if "messages" not in st.session_state:

    st.session_state.messages = get_chat_history()


# Main heading
st.markdown(
    '<div class="main-title">NOVA AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Think Smarter. Learn Faster. Build Better.'
    '</div>',
    unsafe_allow_html=True
)

st.write("")


# Welcome screen
if not st.session_state.messages:

    st.markdown(
        "### Welcome to NOVA AI 👋"
    )

    st.write(
        "Your personal AI assistant for learning, "
        "programming and productivity."
    )

    st.markdown("#### What would you like to explore?")

    col1, col2 = st.columns(2)

    with col1:
        if st.button(
            "🐍 Learn Python",
            use_container_width=True
        ):
            st.session_state.messages.append({
                "role": "user",
                "content": "Teach me Python programming."
            })
            st.rerun()

    with col2:
        if st.button(
            "🧠 Explore AI & ML",
            use_container_width=True
        ):
            st.session_state.messages.append({
                "role": "user",
                "content": "Explain Artificial Intelligence and Machine Learning."
            })
            st.rerun()


# Display conversation
for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])


# Chat input
user_input = st.chat_input(
    "Message NOVA AI..."
)


# Process user message
if user_input:

    user_message = {
        "role": "user",
        "content": user_input
    }

    st.session_state.messages.append(user_message)

    save_message("user", user_input)

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):

        with st.spinner("NOVA AI is thinking..."):

            try:

                response = get_ai_response(
                    st.session_state.messages
                )

                st.markdown(response)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response
                })

                save_message("assistant", response)

            except Exception as error:

                st.error(
                    f"Unable to generate response: {error}"
                )