import os
from dotenv import load_dotenv
from groq import Groq
import streamlit as st

load_dotenv()

st.set_page_config(
    page_title="Content Generator Studio", page_icon="✍️", layout="centered"
)
st.title("✍️ AI Content Generator Studio")

api_key = os.environ.get("GROQ_API_KEY") or st.sidebar.text_input(
    "Groq API Key", type="password"
)

content_type = st.selectbox(
    "Select Output Format",
    ["SEO Blog Post", "Twitter Thread", "Professional Cold Email"],
)
topic = st.text_input(
    "What is the topic or core message?",
    placeholder="e.g., The future of autonomous drones in logistics",
)
tone = st.selectbox("Tone", ["Professional", "Casual & Witty", "Persuasive"])

if st.button("Generate Content"):
    if not api_key or not topic:
        st.warning("Please make sure you entered an API key and a topic.")
    else:
        client = Groq(api_key=api_key)
        with st.spinner("Drafting content..."):
            prompt = f"Write a {content_type} about '{topic}' with a {tone} tone."
            res = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a master copywriter and content creator.",
                    },
                    {"role": "user", "content": prompt},
                ],
            )
            output = res.choices[0].message.content
            st.subheader("Generated Output")
            st.markdown(output)
            st.download_button(
                "📥 Download Content", output, file_name="ai_content.md"
            )