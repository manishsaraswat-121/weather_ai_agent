"""
Main LangGraph Pipeline for Weather and PDF RAG System
"""

import os
import logging
import requests
from typing import TypedDict, Literal

from dotenv import load_dotenv
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_openai import ChatOpenAI
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_qdrant import QdrantVectorStore
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import StateGraph, END

# ---------------------------------------------------------------------
# Setup
# ---------------------------------------------------------------------

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------
# Graph State
# ---------------------------------------------------------------------

class GraphState(TypedDict):
    query: str
    query_type: Literal["weather", "pdf", "unknown"]
    weather_data: dict
    pdf_context: str
    llm_response: str
    error: str

# ---------------------------------------------------------------------
# AI Agent
# ---------------------------------------------------------------------

class AIAgent:
    """
    AI Agent handling ONLY:
    - Weather queries
    - PDF grounded RAG queries
    """

    def __init__(
        self,
        openai_api_key: str,
        openweather_api_key: str,
        qdrant_url: str = ":memory:",
        langsmith_api_key: str | None = None,
    ):
        self.openai_api_key = openai_api_key
        self.openweather_api_key = openweather_api_key

        # ---------------- LangSmith (Optional & Safe) ----------------
        if langsmith_api_key:
            os.environ["LANGSMITH_PROJECT"] = "weather_api_tracing"

        # ---------------- LLM ----------------
        self.llm = ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0.3,
            api_key=openai_api_key,
            base_url="https://openrouter.ai/api/v1",
            default_headers={
                "HTTP-Referer": "http://localhost",
                "X-Title": "weather-pdf-rag-agent",
            },
        )

        # ---------------- Embeddings ----------------
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

        self.collection_name = "pdf_documents"
        self.vector_store = None

        # ---------------- LangGraph ----------------
        self.graph = self._build_graph()

    # -----------------------------------------------------------------
    # Graph Construction
    # -----------------------------------------------------------------

    def _build_graph(self):
        workflow = StateGraph(GraphState)

        workflow.add_node("router", self.route_query)
        workflow.add_node("fetch_weather", self.fetch_weather)
        workflow.add_node("fetch_pdf_context", self.fetch_pdf_context)
        workflow.add_node("generate_response", self.generate_response)

        workflow.set_entry_point("router")

        workflow.add_conditional_edges(
            "router",
            self.decide_path,
            {
                "weather": "fetch_weather",
                "pdf": "fetch_pdf_context",
                "unknown": "generate_response",
            },
        )

        workflow.add_edge("fetch_weather", "generate_response")
        workflow.add_edge("fetch_pdf_context", "generate_response")
        workflow.add_edge("generate_response", END)

        return workflow.compile()

    # -----------------------------------------------------------------
    # Routing
    # -----------------------------------------------------------------

    def route_query(self, state: GraphState) -> GraphState:
        query = state["query"].lower()

        weather_keywords = [
            "weather", "temperature", "forecast",
            "climate", "rain", "sunny", "cloudy",
        ]

        if any(k in query for k in weather_keywords):
            state["query_type"] = "weather"

        elif self.vector_store is not None:
            state["query_type"] = "pdf"

        else:
            state["query_type"] = "unknown"

        logger.info(f"Query routed to: {state['query_type']}")
        return state

    def decide_path(self, state: GraphState) -> str:
        return state["query_type"]

    # -----------------------------------------------------------------
    # Weather Node
    # -----------------------------------------------------------------

    def fetch_weather(self, state: GraphState) -> GraphState:
        try:
            city = self._extract_city(state["query"])

            response = requests.get(
                "https://api.openweathermap.org/data/2.5/weather",
                params={
                    "q": city,
                    "appid": self.openweather_api_key,
                    "units": "metric",
                },
                timeout=10,
            )
            response.raise_for_status()
            data = response.json()

            state["weather_data"] = {
                "city": data["name"],
                "temperature": data["main"]["temp"],
                "feels_like": data["main"]["feels_like"],
                "description": data["weather"][0]["description"],
                "humidity": data["main"]["humidity"],
                "wind_speed": data["wind"]["speed"],
            }

        except Exception as e:
            logger.error(f"Weather error: {e}")
            state["error"] = "Weather data could not be retrieved."
            state["weather_data"] = {}

        return state

    def _extract_city(self, query: str) -> str:
        prompt = ChatPromptTemplate.from_template(
            "Extract the city name from the query. "
            "If none found, return London.\nQuery: {query}\nCity:"
        )
        try:
            res = (prompt | self.llm).invoke({"query": query})
            return res.content.strip() or "London"
        except Exception:
            return "London"

    # -----------------------------------------------------------------
    # PDF RAG Node
    # -----------------------------------------------------------------

    def fetch_pdf_context(self, state: GraphState) -> GraphState:
        try:
            retriever = self.vector_store.as_retriever(search_kwargs={"k": 3})
            docs = retriever.get_relevant_documents(state["query"])
            state["pdf_context"] = "\n\n".join(d.page_content for d in docs)
        except Exception as e:
            logger.error(f"PDF retrieval error: {e}")
            state["pdf_context"] = ""
        return state

    # -----------------------------------------------------------------
    # STRICT Context Validation (🔥 KEY FIX 🔥)
    # -----------------------------------------------------------------

    def _is_context_relevant(self, query: str, context: str) -> bool:
        if not context.strip():
            return False

        query_terms = set(query.lower().split())
        context_terms = set(context.lower().split())

        overlap = query_terms.intersection(context_terms)

        return len(overlap) >= 2

    # -----------------------------------------------------------------
    # Response Generation
    # -----------------------------------------------------------------

    def generate_response(self, state: GraphState) -> GraphState:
        try:
            if state["query_type"] == "weather":
                w = state["weather_data"]
                prompt = ChatPromptTemplate.from_template(
                    "Weather details:\n"
                    "City: {city}\n"
                    "Temperature: {temperature}°C\n"
                    "Feels Like: {feels_like}°C\n"
                    "Condition: {description}\n"
                    "Humidity: {humidity}%\n"
                    "Wind Speed: {wind_speed} m/s\n\n"
                    "Answer the query: {query}"
                )
                res = (prompt | self.llm).invoke({**w, "query": state["query"]})
                state["llm_response"] = res.content

            elif state["query_type"] == "pdf":

                if not self._is_context_relevant(
                    state["query"], state["pdf_context"]
                ):
                    state["llm_response"] = (
                        "Please ask a question strictly related to the "
                        "uploaded PDF documents. I cannot answer general "
                        "knowledge questions."
                    )
                    return state

                prompt = ChatPromptTemplate.from_template(
                    "Answer ONLY using the context below. "
                    "If the answer is not present, say so explicitly.\n\n"
                    "Context:\n{context}\n\n"
                    "Question: {query}\nAnswer:"
                )

                res = (prompt | self.llm).invoke(
                    {"context": state["pdf_context"], "query": state["query"]}
                )
                state["llm_response"] = res.content

            else:
                state["llm_response"] = (
                    "Please ask a weather-related question or a question "
                    "based on the available PDF documents."
                )

        except Exception as e:
            logger.error(f"LLM error: {e}")
            state["llm_response"] = "An error occurred while generating the response."

        return state

    # -----------------------------------------------------------------
    # PDF Loader
    # -----------------------------------------------------------------

    def load_pdf(self, pdf_path: str) -> bool:
        try:
            loader = PyPDFLoader(pdf_path)
            docs = loader.load()

            splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200,
            )
            splits = splitter.split_documents(docs)

            self.vector_store = QdrantVectorStore.from_documents(
                documents=splits,
                embedding=self.embeddings,
                location=":memory:",
                collection_name=self.collection_name,
            )

            logger.info("PDF loaded and indexed successfully")
            return True

        except Exception as e:
            logger.error(f"PDF load error: {e}")
            return False

    # -----------------------------------------------------------------
    # Public Query API
    # -----------------------------------------------------------------

    def query(self, user_query: str) -> dict:
        state: GraphState = {
            "query": user_query,
            "query_type": "unknown",
            "weather_data": {},
            "pdf_context": "",
            "llm_response": "",
            "error": "",
        }
        return self.graph.invoke(state)
