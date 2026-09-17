import streamlit as st

st.set_page_config(
    page_title="AI Studio Pro", page_icon="🚀", layout="centered"
)

st.title("🚀 Welcome to AI Studio Pro")
st.markdown(
    """
    ### Your All-in-One Generative AI Workspace
    This platform brings enterprise-grade AI capabilities straight to your browser. 
    Use the sidebar navigation to switch between tools:
    
    * **🤖 AI Chatbot Studio:** Talk to custom specialized AI personas with full context retention.
    * **📄 Document Summarizer & Q&A:** Upload PDFs or text files to extract insights and chat with your documents.
    * **✍️ Content Generator Studio:** Instantly generate SEO-optimized blog posts, tweets, or emails.
    """
)

st.info("👈 Use the sidebar menu to navigate between the apps.")

# Quick metric cards
col1, col2, col3 = st.columns(3)
col1.metric("Available Models", "Llama 3.3 70B", "Fast Inference")
col2.metric("Uptime", "99.9%", "Cloud Ready")
col3.metric("Security", "In-Memory / Secure", "Encrypted")