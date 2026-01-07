"""
Streamlit UI for Weather and PDF RAG Agent
"""

# ===================== 🔥 CRITICAL FIX 🔥 =====================
import os
os.environ["STREAMLIT_WATCHER_TYPE"] = "none"
# =============================================================

import streamlit as st
import tempfile
import logging
from main import AIAgent

# ---------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------
# Page Config
# ---------------------------------------------------------------------
st.set_page_config(
    page_title="AI Agent - Weather & PDF RAG",
    page_icon="🤖",
    layout="wide"
)

# ---------------------------------------------------------------------
# Styling
# ---------------------------------------------------------------------
st.markdown("""
<style>
.main-header {
    font-size: 2.4rem;
    font-weight: 700;
    color: #1E88E5;
    text-align: center;
    margin-bottom: 0.25rem;
}
.sub-header {
    font-size: 1.1rem;
    color: #666;
    text-align: center;
    margin-bottom: 1.5rem;
}
div[data-testid="chat-message"] {
    font-size: 1.05rem;
    line-height: 1.6;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------
# Agent Initialization
# ---------------------------------------------------------------------
def initialize_agent():
    openai_key = os.getenv("OPENAI_API_KEY") or st.session_state.get("openai_key")
    weather_key = os.getenv("OPENWEATHER_API_KEY") or st.session_state.get("weather_key")
    langsmith_key = os.getenv("LANGSMITH_API_KEY") or st.session_state.get("langsmith_key")

    if not openai_key or not weather_key:
        return None

    try:
        return AIAgent(
            openai_api_key=openai_key,
            openweather_api_key=weather_key,
            langsmith_api_key=langsmith_key
        )
    except Exception as e:
        st.error(f"Agent initialization failed: {e}")
        return None

# ---------------------------------------------------------------------
# Main App
# ---------------------------------------------------------------------
def main():
    # Header
    st.markdown('<div class="main-header">🤖 AI Agent – Weather & PDF RAG</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Ask about weather or upload a PDF to query</div>', unsafe_allow_html=True)

    # Session State
    st.session_state.setdefault("messages", [])
    st.session_state.setdefault("agent", None)
    st.session_state.setdefault("pdf_loaded", False)

    # -----------------------------------------------------------------
    # Sidebar
    # -----------------------------------------------------------------
    with st.sidebar:
        st.header("⚙️ Configuration")

        with st.expander("🔑 API Keys", expanded=not st.session_state.agent):
            st.session_state.openai_key = st.text_input("OpenAI / OpenRouter API Key", type="password")
            st.session_state.weather_key = st.text_input("OpenWeather API Key", type="password")
            st.session_state.langsmith_key = st.text_input("LangSmith API Key (Optional)", type="password")

            if st.button("💾 Initialize Agent"):
                st.session_state.agent = initialize_agent()
                if st.session_state.agent:
                    st.success("✅ Agent initialized")
                else:
                    st.error("❌ Missing or invalid API keys")

        st.header("📄 PDF Upload")
        uploaded_file = st.file_uploader("Upload a PDF document", type=["pdf"])

        if uploaded_file and st.session_state.agent:
            if st.button("📤 Load PDF"):
                with st.spinner("Processing PDF..."):
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                        tmp.write(uploaded_file.getvalue())
                        tmp_path = tmp.name

                    success = st.session_state.agent.load_pdf(tmp_path)
                    os.unlink(tmp_path)

                    if success:
                        st.session_state.pdf_loaded = True
                        st.success("✅ PDF loaded & indexed")
                    else:
                        st.error("❌ PDF loading failed")

        if st.button("🗑️ Clear Chat"):
            st.session_state.messages.clear()
            st.rerun()

    # -----------------------------------------------------------------
    # Chat Area
    # -----------------------------------------------------------------
    if not st.session_state.agent:
        st.info("⚠️ Please configure your API keys from the sidebar to begin.")
        return

    # Display chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Chat input
    if prompt := st.chat_input("Ask about weather or your uploaded PDF…"):
        # User message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Assistant response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    result = st.session_state.agent.query(prompt)
                    response = result.get("llm_response", "No response generated.")

                    st.session_state.messages.append(
                        {"role": "assistant", "content": response}
                    )
                    st.markdown(response)

                except Exception as e:
                    st.error(str(e))

    # Footer
    st.markdown("---")
    st.markdown(
        "<center style='color:#777'>Built with LangChain, LangGraph, Qdrant & Streamlit</center>",
        unsafe_allow_html=True
    )

# ---------------------------------------------------------------------
# Entry Point
# ---------------------------------------------------------------------
if __name__ == "__main__":
    main()
