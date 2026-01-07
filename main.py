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

#from qdrant_client import QdrantClient

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
    """Main AI Agent handling weather and PDF queries"""

    def __init__(
        self,
        openai_api_key: str,
        openweather_api_key: str,
        qdrant_url: str = ":memory:",
        langsmith_api_key: str | None = None,
    ):
        self.openai_api_key = openai_api_key
        self.openweather_api_key = openweather_api_key

        # ---------------- LangSmith (SAFE) ----------------
        if langsmith_api_key:
            #os.environ["LANGSMITH_TRACING"] = "true"
            #os.environ["LANGSMITH_API_KEY"] = langsmith_api_key
            os.environ["LANGSMITH_PROJECT"] = "weather_api_tracing"

        # ---------------- LLM (OpenRouter) ----------------
        self.llm = ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0.7,
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


        # ---------------- Qdrant (RESTORED + FIXED) ----------------
        '''if qdrant_url == ":memory:":
            self.qdrant_client = QdrantClient(":memory:")
        else:
            self.qdrant_client = QdrantClient(url=qdrant_url)'''

        self.collection_name = "pdf_documents"
        self.vector_store = None

        # ---------------- Graph ----------------
        self.graph = self._build_graph()

    # -----------------------------------------------------------------
    # LangGraph
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
            "weather",
            "temperature",
            "forecast",
            "climate",
            "rain",
            "sunny",
            "cloudy",
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

            url = "https://api.openweathermap.org/data/2.5/weather"
            params = {
                "q": city,
                "appid": self.openweather_api_key,
                "units": "metric",
            }

            response = requests.get(url, params=params, timeout=10)
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
            state["weather_data"] = {}
            state["error"] = "Weather data could not be retrieved."

        return state

    def _extract_city(self, query: str) -> str:
        prompt = ChatPromptTemplate.from_template(
            "Extract the city name from the query. "
            "If none found, return London.\nQuery: {query}\nCity:"
        )
        try:
            chain = prompt | self.llm
            result = chain.invoke({"query": query})
            return result.content.strip() or "London"
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
    # Response Generation
    # -----------------------------------------------------------------

    def generate_response(self, state: GraphState) -> GraphState:
        try:
            if state["query_type"] == "weather":
                w = state["weather_data"]
                prompt = ChatPromptTemplate.from_template(
                    "Weather details:\n"
                    "City: {city}\n"
                    "Temp: {temperature}°C (Feels like {feels_like}°C)\n"
                    "Condition: {description}\n"
                    "Humidity: {humidity}%\n"
                    "Wind: {wind_speed} m/s\n\n"
                    "Answer the user query: {query}"
                )
                res = (prompt | self.llm).invoke({**w, "query": state["query"]})
                state["llm_response"] = res.content

            elif state["query_type"] == "pdf":
                prompt = ChatPromptTemplate.from_template(
                    "Use the context below to answer the question.\n\n"
                    "Context:\n{context}\n\n"
                    "Question: {query}\nAnswer:"
                )
                res = (prompt | self.llm).invoke(
                    {"context": state["pdf_context"], "query": state["query"]}
                )
                state["llm_response"] = res.content

            else:
                state["llm_response"] = (
                    "I couldn't determine whether this is a weather or document query."
                )

        except Exception as e:
            logger.error(f"LLM error: {e}")
            state["llm_response"] = str(e)

        return state

    # -----------------------------------------------------------------
    # PDF Loader (✅ FIXED & WORKING)
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
                location=":memory:",        # 🔥 THIS IS THE FIX
                collection_name="pdf_documents",
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

# ---------------------------------------------------------------------
# Example Run
# ---------------------------------------------------------------------

if __name__ == "__main__":
    agent = AIAgent(
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        openweather_api_key=os.getenv("OPENWEATHER_API_KEY"),
        langsmith_api_key=os.getenv("LANGSMITH_API_KEY"),
    )

    result = agent.query("What's the weather in Paris?")
    print("\nResponse:\n", result["llm_response"])
