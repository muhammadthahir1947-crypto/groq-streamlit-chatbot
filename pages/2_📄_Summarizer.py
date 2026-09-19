import os
from dotenv import load_dotenv
from groq import Groq
from pypdf import PdfReader
import streamlit as st

load_dotenv()

st.set_page_config(
    page_title="Document Summarizer", page_icon="📄", layout="centered"
)
st.title("📄 Document Summarizer & Q&A")

api_key = os.environ.get("GROQ_API_KEY") or st.sidebar.text_input(
    "Groq API Key", type="password"
)

uploaded_file = st.file_uploader("Upload PDF or TXT", type=["pdf", "txt"])

if uploaded_file:
    text = ""
    if uploaded_file.type == "application/pdf":
        reader = PdfReader(uploaded_file)
        for page in reader.pages:
            t = page.extract_text()
            if t:
                text += t + "\n"
    else:
        text = uploaded_file.read().decode("utf-8")

    if text.strip():
        st.success(f"Loaded file successfully ({len(text)} characters)")

        if st.button("Generate Executive Summary"):
            if not api_key:
                st.warning("API key missing.")
            else:
                client = Groq(api_key=api_key)
                with st.spinner("Summarizing..."):
                    res = client.chat.completions.create(
                        model="openai/gpt-oss-120b",
                        messages=[
                            {
                                "role": "system",
                                "content": "Summarize clearly with key bullet points.",
                            },
                            {
                                "role": "user",
                                "content": text[:12000],
                            },
                        ],
                    )
                    st.subheader("Summary")
                    st.markdown(res.choices[0].message.content)