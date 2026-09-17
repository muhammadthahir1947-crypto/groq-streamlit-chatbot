import os
from dotenv import load_dotenv
from groq import Groq
import streamlit as st

load_dotenv()

st.set_page_config(
    page_title="AI Chatbot Studio", page_icon="🤖", layout="centered"
)
st.title("🤖 AI Persona Chat Studio")

# API Key handling (checks .env first, then sidebar input)
api_key = os.environ.get("GROQ_API_KEY") or st.sidebar.text_input(
    "Groq API Key", type="password"
)

persona = st.selectbox(
    "Choose AI Persona:",
    [
        "Friendly Assistant",
        "Sarcastic Senior Developer",
        "Aggressive Startup Pitch Coach",
        "Philosophical Sage",
    ],
)

system_prompts = {
    "Friendly Assistant": "You are a warm, helpful, and exceptionally friendly AI assistant.",
    "Sarcastic Senior Developer": "You are a cynical, highly experienced senior software developer who loves sarcasm and clean code.",
    "Aggressive Startup Pitch Coach": "You are a fierce, no-nonsense Silicon Valley venture capitalist. Tear down bad ideas and push for high growth.",
    "Philosophical Sage": "You speak in deep, thought-provoking metaphors, drawing from ancient philosophies.",
}

if "messages" not in st.session_state:
    st.session_state.messages = []

if st.sidebar.button("Clear Chat History"):
    st.session_state.messages = []
    st.rerun()

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Say something..."):
    if not api_key:
        st.warning("Please provide a Groq API key.")
    else:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        client = Groq(api_key=api_key)
        with st.chat_message("assistant"):
            placeholder = st.empty()
            full_resp = ""
            payload = [{"role": "system", "content": system_prompts[persona]}] + [
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ]

            try:
                stream = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=payload,
                    stream=True,
                )
                for chunk in stream:
                    if chunk.choices[0].delta.content:
                        full_resp += chunk.choices[0].delta.content
                        placeholder.markdown(full_resp + "▌")
                placeholder.markdown(full_resp)
                st.session_state.messages.append(
                    {"role": "assistant", "content": full_resp}
                )
            except Exception as e:
                st.error(f"Error: {e}")