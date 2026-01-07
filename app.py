"""
Streamlit UI for Weather and PDF RAG Agent
PDFs are auto-loaded from sample_docs/
"""

# ===================== 🔥 CRITICAL FIX 🔥 =====================
import os
os.environ["STREAMLIT_WATCHER_TYPE"] = "none"
# =============================================================

import streamlit as st
import logging
from dotenv import load_dotenv
from main import AIAgent

# ---------------------------------------------------------------------
# Load environment variables
# ---------------------------------------------------------------------
load_dotenv()

# ---------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------
PDF_DIRECTORY = "sample_docs"

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
def initialize_agent(use_langsmith: bool):
    """
    Initialize AI Agent and auto-load PDFs from sample_docs/
    """

    openai_key = os.getenv("OPENAI_API_KEY")
    weather_key = os.getenv("OPENWEATHER_API_KEY")
    langsmith_key = os.getenv("LANGSMITH_API_KEY") if use_langsmith else None

    if not openai_key or not weather_key:
        st.error("❌ Required API keys missing in .env file")
        return None

    try:
        agent = AIAgent(
            openai_api_key=openai_key,
            openweather_api_key=weather_key,
            langsmith_api_key=langsmith_key
        )

        # ------------------ AUTO LOAD PDFs ------------------
        if os.path.exists(PDF_DIRECTORY):
            pdf_files = [
                os.path.join(PDF_DIRECTORY, f)
                for f in os.listdir(PDF_DIRECTORY)
                if f.lower().endswith(".pdf")
            ]

            if not pdf_files:
                st.warning("⚠️ No PDFs found in sample_docs/")
            else:
                with st.spinner("Indexing PDFs from sample_docs/..."):
                    for pdf_path in pdf_files:
                        agent.load_pdf(pdf_path)

                st.success(f"📄 Loaded {len(pdf_files)} PDF(s) from sample_docs/")

        else:
            st.warning("⚠️ sample_docs/ directory not found")

        return agent

    except Exception as e:
        logger.exception("Agent initialization failed")
        st.error(f"Agent initialization failed: {e}")
        return None

# ---------------------------------------------------------------------
# Main App
# ---------------------------------------------------------------------
def main():
    # Header
    st.markdown('<div class="main-header">🤖 AI Agent – Weather & PDF RAG</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sub-header">Weather queries & document Q&A using LangGraph</div>',
        unsafe_allow_html=True
    )

    # Session State
    st.session_state.setdefault("messages", [])
    st.session_state.setdefault("agent", None)
    st.session_state.setdefault("use_langsmith", False)

    # -----------------------------------------------------------------
    # Sidebar
    # -----------------------------------------------------------------
    with st.sidebar:
        st.header("⚙️ Agent Controls")

        st.session_state.use_langsmith = st.toggle(
            "Enable LangSmith Tracing",
            value=False,
            help="Uses LANGSMITH_API_KEY from .env"
        )

        if st.button("🚀 Initialize Agent"):
            st.session_state.agent = initialize_agent(
                use_langsmith=st.session_state.use_langsmith
            )

            if st.session_state.agent:
                st.success("✅ Agent initialized successfully")

        st.divider()

        st.markdown("### 📄 Knowledge Source")
        st.markdown(
            f"""
            **PDF Source:**  
            `{PDF_DIRECTORY}/`

            All PDFs in this folder are automatically indexed at startup.
            """
        )

        if st.button("🗑️ Clear Chat"):
            st.session_state.messages.clear()
            st.rerun()

    # -----------------------------------------------------------------
    # Chat Area
    # -----------------------------------------------------------------
    if not st.session_state.agent:
        st.info("ℹ️ Initialize the agent from the sidebar to begin.")
        return

    # Display chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Chat input
    if prompt := st.chat_input("Ask about weather or the indexed PDFs…"):
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

                except Exception:
                    logger.exception("Query processing failed")
                    st.error("Something went wrong while processing the query.")

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
