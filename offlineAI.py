import streamlit as st
import ollama

# ==================================================
# PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="Offline AI",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ==================================================
# LOAD CSS
# ==================================================

try:
    with open("style.css", "r", encoding="utf-8") as file:
        css = file.read()
        st.markdown(
            f"<style>{css}</style>",
            unsafe_allow_html=True
        )
except FileNotFoundError:
    st.error("style.css file not found. Keep it in the same folder as offlineAI.py.")

# ==================================================
# CHAT MEMORY
# ==================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

# ==================================================
# HEADER
# =================================================

# ==================================================
# WELCOME SCREEN
# ==================================================

st.markdown(
    """
    <style>

    .welcome-box {
        background: linear-gradient(135deg, #444444, #292929);
        border-radius: 28px;
        padding: 75px 40px;
        margin: 120px auto 40px auto;
        width: 75%;
        text-align: center;
        box-shadow: 0 10px 35px rgba(0, 0, 0, 0.45);
        border: 1px solid rgba(255, 255, 255, 0.08);
    }

    .welcome-text {
        color: #ffffff;
        font-family: "Segoe UI", sans-serif;
        font-size: 44px;
        font-weight: 600;
        letter-spacing: 0.5px;
    }

    </style>
    """,
    unsafe_allow_html=True
)

if not st.session_state.messages:

    st.markdown(
        """
        <div class="welcome-box">
            <div class="welcome-text">
                I'm your personal AI assistant.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
# ==================================================
# DISPLAY CHAT HISTORY
# ==================================================

for message in st.session_state.messages:

    avatar = "👤" if message["role"] == "user" else "🤖"

    with st.chat_message(
        message["role"],
        avatar=avatar
    ):
        st.markdown(message["content"])

# ==================================================
# CHAT INPUT
# ==================================================

prompt = st.chat_input(
    "Message Offline AI..."
)

# ==================================================
# SEND MESSAGE
# ==================================================

if prompt:

    # ----------------------------------------------
    # USER MESSAGE
    # ----------------------------------------------

    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    # ----------------------------------------------
    # AI RESPONSE
    # ----------------------------------------------

    with st.chat_message("assistant", avatar="🤖"):

        with st.spinner("Thinking..."):

            try:

                response = ollama.chat(
                    model="llama3.2",
                    messages=st.session_state.messages
                )

                answer = response["message"]["content"]

                st.markdown(answer)

                # Save AI response
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer
                })

            except Exception as error:

                st.error("❌ Could not connect to Ollama.")

                st.info(
                    "Make sure Ollama is running and "
                    "the llama3.2 model is installed."
                )

                st.code(str(error))