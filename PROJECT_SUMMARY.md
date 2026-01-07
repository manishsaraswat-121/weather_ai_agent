# AI Agent Pipeline - Project Summary

## 🎯 Project Overview

This is a **production-grade AI pipeline** that demonstrates advanced LangChain, LangGraph, and RAG concepts through an intelligent agent system capable of:

1. **Real-time Weather Queries** - Fetches current weather data via OpenWeatherMap API
2. **PDF Document Q&A** - Answers questions from uploaded PDFs using RAG

The system intelligently routes queries to the appropriate handler and generates natural language responses using GPT-3.5-turbo.

---

## 🏗️ Technical Architecture

### Core Technologies

| Technology | Purpose | Version |
|------------|---------|---------|
| **LangChain** | LLM orchestration framework | 0.3.13 |
| **LangGraph** | Agentic workflow engine | 0.2.59 |
| **LangSmith** | LLM observability & evaluation | 0.2.5 |
| **Qdrant** | Vector database for embeddings | 1.12.1 |
| **OpenAI** | LLM (GPT-3.5-turbo) & embeddings | Latest |
| **Streamlit** | Web UI framework | 1.41.1 |
| **Pytest** | Testing framework | 8.3.4 |

### System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Streamlit UI Layer                    │
│              (User Interface & Interaction)              │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│                 LangGraph Pipeline                       │
│  ┌────────────────────────────────────────────────┐     │
│  │         Router Node (Query Classifier)         │     │
│  │  Analyzes query → Decides: Weather or PDF      │     │
│  └───────────┬──────────────────┬─────────────────┘     │
│              │                  │                        │
│    ┌─────────▼────────┐  ┌─────▼──────────┐            │
│    │  Weather Node    │  │   PDF RAG Node  │            │
│    │ • Extract city   │  │ • Vector search │            │
│    │ • Call API       │  │ • Retrieve docs │            │
│    │ • Parse data     │  │ • Build context │            │
│    └─────────┬────────┘  └─────┬──────────┘            │
│              │                  │                        │
│              └────────┬─────────┘                        │
│                       │                                  │
│              ┌────────▼─────────┐                        │
│              │ Response Generator│                       │
│              │ • GPT-3.5-turbo  │                        │
│              │ • Generate answer│                        │
│              └──────────────────┘                        │
└─────────────────────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│              External Services Layer                     │
│  ┌──────────┐  ┌────────┐  ┌────────┐  ┌──────────┐   │
│  │  OpenAI  │  │Qdrant  │  │Weather │  │LangSmith │   │
│  │   API    │  │ Vector │  │  API   │  │ Tracking │   │
│  │          │  │   DB   │  │        │  │          │   │
│  └──────────┘  └────────┘  └────────┘  └──────────┘   │
└─────────────────────────────────────────────────────────┘
```

---

## 📦 Deliverables Checklist

### ✅ Code Repository
- [x] `main.py` - Core LangGraph pipeline (450+ lines)
- [x] `app.py` - Streamlit UI (350+ lines)
- [x] `test_main.py` - Comprehensive unit tests (400+ lines)
- [x] `requirements.txt` - All dependencies
- [x] `.env.example` - Environment template
- [x] `.gitignore` - Security configuration

### ✅ Documentation
- [x] `README.md` - Complete project documentation
- [x] `SETUP_GUIDE.md` - Detailed setup instructions
- [x] `QUICK_REFERENCE.md` - Quick command reference
- [x] `PROJECT_SUMMARY.md` - This file
- [x] `SUBMISSION_CHECKLIST.md` - Pre-submission guide

### ✅ Automation
- [x] `run.sh` - Quick start for Linux/Mac
- [x] `run.bat` - Quick start for Windows
- [x] `.github/workflows/tests.yml` - CI/CD pipeline
- [x] `create_package.py` - Package creator script

### ✅ Testing
- [x] Unit tests for all core functions
- [x] Integration tests for end-to-end flow
- [x] Mock tests for external APIs
- [x] Error handling tests
- [x] Coverage report generation

### ✅ UI/UX
- [x] Clean chat interface
- [x] API key configuration
- [x] PDF upload functionality
- [x] Real-time status indicators
- [x] Debug information panels
- [x] Responsive design

---

## 🔑 Key Features Implemented

### 1. Intelligent Query Routing ✅

**Location**: `main.py` - `route_query()` method

The router node analyzes incoming queries using keyword matching and vector store availability:

```python
def route_query(self, state: GraphState) -> GraphState:
    query = state["query"].lower()
    weather_keywords = ["weather", "temperature", "forecast", ...]
    
    if any(keyword in query for keyword in weather_keywords):
        state["query_type"] = "weather"
    elif self.vector_store is not None:
        state["query_type"] = "pdf"
    else:
        state["query_type"] = "unknown"
```

**Enhancement Opportunity**: Could use semantic similarity with embeddings for more accurate routing.

### 2. Real-time Weather Integration ✅

**Location**: `main.py` - `fetch_weather()` method

Integrates with OpenWeatherMap API to fetch current weather:

```python
def fetch_weather(self, state: GraphState) -> GraphState:
    # Extract city using LLM
    city = self._extract_city(state["query"])
    
    # Call OpenWeatherMap API
    response = requests.get(url, params={...})
    data = response.json()
    
    # Store structured weather data
    state["weather_data"] = {
        "city": data["name"],
        "temperature": data["main"]["temp"],
        "description": data["weather"][0]["description"],
        ...
    }
```

**Features**:
- LLM-based city extraction from natural language
- Comprehensive error handling
- Metric units (Celsius)
- Multiple weather parameters

### 3. PDF RAG System ✅

**Location**: `main.py` - `load_pdf()` and `fetch_pdf_context()` methods

Full RAG pipeline implementation:

#### A. Document Processing
```python
def load_pdf(self, pdf_path: str):
    # Load PDF
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()
    
    # Split into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    splits = text_splitter.split_documents(documents)
    
    # Generate embeddings and store in Qdrant
    self.vector_store = QdrantVectorStore.from_documents(
        splits,
        self.embeddings,
        collection_name=self.collection_name
    )
```

#### B. Retrieval
```python
def fetch_pdf_context(self, state: GraphState) -> GraphState:
    retriever = self.vector_store.as_retriever(search_kwargs={"k": 3})
    docs = retriever.get_relevant_documents(state["query"])
    context = "\n\n".join([doc.page_content for doc in docs])
    state["pdf_context"] = context
```

**Features**:
- Efficient chunking strategy (1000 chars, 200 overlap)
- OpenAI ada-002 embeddings (1536 dimensions)
- Cosine similarity search
- Top-3 document retrieval

### 4. LLM Response Generation ✅

**Location**: `main.py` - `generate_response()` method

Context-aware response generation using GPT-3.5-turbo:

```python
def generate_response(self, state: GraphState) -> GraphState:
    if query_type == "weather":
        prompt = ChatPromptTemplate.from_template(
            "Based on the following weather data, provide a helpful response...\n"
            "Weather Data: {weather_data}\n"
            "Query: {query}"
        )
    elif query_type == "pdf":
        prompt = ChatPromptTemplate.from_template(
            "Based on the following context, answer the question...\n"
            "Context: {context}\n"
            "Question: {query}"
        )
```

**Features**:
- Template-based prompting
- Context injection
- Natural language output
- Error recovery

### 5. LangSmith Integration ✅

**Location**: `main.py` - `__init__()` method

Automatic tracing and evaluation:

```python
if langsmith_api_key:
    os.environ["LANGCHAIN_TRACING_V2"] = "true"
    os.environ["LANGCHAIN_API_KEY"] = langsmith_api_key
    os.environ["LANGCHAIN_PROJECT"] = "weather-pdf-rag-agent"
```

**Tracked Metrics**:
- All LLM calls and responses
- Token usage and costs
- Latency per operation
- Success/failure rates
- Full conversation traces

### 6. Vector Database (Qdrant) ✅

**Location**: Throughout `main.py`

In-memory vector store with production-ready configuration:

```python
self.qdrant_client.create_collection(
    collection_name=self.collection_name,
    vectors_config=VectorParams(
        size=1536,  # OpenAI ada-002 dimension
        distance=Distance.COSINE
    )
)
```

**Features**:
- In-memory mode (fast prototyping)
- Persistent storage capable
- Cosine similarity search
- Automatic collection management

### 7. Streamlit UI ✅

**Location**: `app.py`

Professional chat interface with full functionality:

**Key Components**:
- Chat history display
- Real-time message streaming
- API key configuration panel
- PDF upload and processing
- Status indicators
- Debug information
- Error handling
- Responsive design

**Features**:
- Session state management
- File upload handling
- Configuration persistence
- Clean, modern design
- Mobile-responsive

---

## 🧪 Testing Strategy

### Test Coverage

**Location**: `test_main.py`

Comprehensive test suite covering:

#### 1. Unit Tests
- ✅ Agent initialization
- ✅ Query routing logic
- ✅ Weather API integration (mocked)
- ✅ PDF processing
- ✅ Vector database operations
- ✅ LLM response generation
- ✅ Error handling

#### 2. Integration Tests
- ✅ End-to-end query flow
- ✅ State management
- ✅ Graph execution

#### 3. Mock Strategy
```python
@patch('main.ChatOpenAI')
@patch('main.OpenAIEmbeddings')
@patch('main.QdrantClient')
def test_agent_initialization(self, mock_qdrant, mock_embeddings, mock_llm):
    agent = AIAgent(...)
    self.assertIsNotNone(agent)
```

### Running Tests

```bash
# Basic test run
pytest test_main.py -v

# With coverage report
pytest test_main.py --cov=main --cov-report=html

# Specific test
pytest test_main.py::TestAIAgent::test_route_query_weather -v
```

**Expected Coverage**: >85%

---

## 🎨 User Experience

### Workflow

1. **Initial Setup**
   - User configures API keys in sidebar
   - System initializes agent

2. **Weather Queries**
   - User asks about weather
   - System extracts city
   - Fetches real-time data
   - Generates natural response

3. **PDF Queries**
   - User uploads PDF
   - System processes and indexes
   - User asks questions
   - System retrieves relevant context
   - Generates contextual answers

### Example Interactions

**Weather Query**:
```
User: "What's the weather like in Tokyo?"
