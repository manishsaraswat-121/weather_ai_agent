# System Architecture

## 🏗️ High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE                           │
│                      (Streamlit Web App)                         │
│  ┌──────────────┐  ┌──────────────┐  ┌────────────────────┐   │
│  │ Chat Input   │  │ PDF Upload   │  │ Config Panel       │   │
│  │ & Display    │  │ Handler      │  │ (API Keys)         │   │
│  └──────────────┘  └──────────────┘  └────────────────────┘   │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                    APPLICATION LAYER                             │
│                    (main.py - AIAgent)                           │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              LangGraph State Machine                      │  │
│  │                                                            │  │
│  │   [Entry] ──→ [Router Node]                              │  │
│  │                      │                                     │  │
│  │                  Decision                                  │  │
│  │                      │                                     │  │
│  │        ┌─────────────┴─────────────┐                     │  │
│  │        │                           │                      │  │
│  │        ▼                           ▼                      │  │
│  │  [Weather Node]              [PDF RAG Node]              │  │
│  │  • Extract city              • Vector search             │  │
│  │  • Call API                  • Retrieve context          │  │
│  │  • Parse response            • Rank results              │  │
│  │        │                           │                      │  │
│  │        └─────────────┬─────────────┘                     │  │
│  │                      │                                     │  │
│  │                      ▼                                     │  │
│  │            [Response Generator Node]                      │  │
│  │            • Build prompt                                 │  │
│  │            • Call LLM                                     │  │
│  │            • Format output                                │  │
│  │                      │                                     │  │
│  │                      ▼                                     │  │
│  │                   [END]                                    │  │
│  └────────────────────────────────────────────────────────────┘  │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                    SERVICES LAYER                                │
│                                                                   │
│  ┌──────────────┐  ┌──────────────┐  ┌────────────────────┐   │
│  │   OpenAI     │  │   Qdrant     │  │  OpenWeatherMap    │   │
│  │              │  │              │  │                     │   │
│  │ • GPT-3.5    │  │ • Vector DB  │  │ • Weather API      │   │
│  │ • Embeddings │  │ • Cosine     │  │ • Real-time data   │   │
│  │ • ada-002    │  │   similarity │  │ • City search      │   │
│  └──────────────┘  └──────────────┘  └────────────────────┘   │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                    LangSmith                              │  │
│  │  • Trace all LLM calls                                    │  │
│  │  • Track token usage                                      │  │
│  │  • Monitor performance                                    │  │
│  │  • Evaluate responses                                     │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🔄 Request Flow Diagrams

### Weather Query Flow

```
User Query: "What's the weather in Paris?"
    │
    ▼
┌─────────────────────┐
│  Router Node        │
│  Detects: "weather" │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Weather Node       │
└──────────┬──────────┘
           │
           ├──→ Extract City
           │    "Paris"
           │
           ├──→ Call OpenWeather API
           │    GET /weather?q=Paris
           │
           ├──→ Parse Response
           │    {temp: 18°C, desc: "sunny"}
           │
           ▼
┌─────────────────────┐
│ Response Generator  │
└──────────┬──────────┘
           │
           ├──→ Build Prompt
           │    "Based on weather data..."
           │
           ├──→ Call GPT-3.5
           │    Generate natural response
           │
           ▼
     Final Response
     "The weather in Paris is 
      currently 18°C and sunny..."
```

### PDF Query Flow

```
User Query: "What is the main topic?"
    │
    ▼
┌─────────────────────┐
│  Router Node        │
│  Detects: "pdf"     │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  PDF RAG Node       │
└──────────┬──────────┘
           │
           ├──→ Generate Query Embedding
           │    [0.023, -0.14, 0.089, ...]
           │
           ├──→ Vector Search (Qdrant)
           │    Cosine similarity
           │    Top 3 chunks
           │
           ├──→ Retrieve Context
           │    "Chunk 1: ...
           │     Chunk 2: ...
           │     Chunk 3: ..."
           │
           ▼
┌─────────────────────┐
│ Response Generator  │
└──────────┬──────────┘
           │
           ├──→ Build Prompt
           │    "Context: {chunks}
           │     Question: {query}"
           │
           ├──→ Call GPT-3.5
           │    Generate answer from context
           │
           ▼
     Final Response
     "The document discusses 
      machine learning concepts..."
```

---

## 📊 Data Flow Architecture

### PDF Processing Pipeline

```
PDF Upload
    │
    ▼
┌──────────────────┐
│  PyPDFLoader     │  Load PDF file
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Text Extractor  │  Extract text from pages
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Text Splitter   │  Split into chunks
│  • Size: 1000    │  (1000 chars, 200 overlap)
│  • Overlap: 200  │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Embeddings      │  Generate vectors
│  Generator       │  (OpenAI ada-002)
│  • Dimension:    │
│    1536          │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Qdrant Vector   │  Store embeddings
│  Database        │  with metadata
└──────────────────┘
```

### Query Processing Pipeline

```
User Query
    │
    ▼
┌──────────────────┐
│  Query Analysis  │  Classify query type
└────────┬─────────┘
         │
    ┌────┴────┐
    │         │
    ▼         ▼
┌───────┐ ┌──────┐
│Weather│ │ PDF  │
│ Path  │ │ Path │
└───┬───┘ └───┬──┘
    │         │
    │         ▼
    │    ┌──────────────┐
    │    │Query Vector  │  Generate embedding
    │    └──────┬───────┘
    │           │
    │           ▼
    │    ┌──────────────┐
    │    │Vector Search │  Similarity search
    │    └──────┬───────┘
    │           │
    │           ▼
    │    ┌──────────────┐
    │    │Context Docs  │  Top-K results
    │    └──────┬───────┘
    │           │
    └────┬──────┘
         │
         ▼
┌──────────────────┐
│  LLM Processing  │  Generate response
│  (GPT-3.5)       │
└────────┬─────────┘
         │
         ▼
   Final Response
```

---

## 🧩 Component Architecture

### Main Components

```
AIAgent
├── LangGraph Workflow
│   ├── Router Node
│   ├── Weather Node
│   ├── PDF RAG Node
│   └── Response Generator
│
├── LLM Interface
│   ├── ChatOpenAI (GPT-3.5)
│   └── Prompts & Templates
│
├── Vector Store
│   ├── Qdrant Client
│   ├── Embeddings (OpenAI)
│   └── Collection Manager
│
├── External APIs
│   ├── OpenWeather Client
│   └── Response Parser
│
└── State Management
    ├── GraphState TypedDict
    └── Session Handler
```

### Streamlit UI Components

```
StreamlitApp
├── Main Interface
│   ├── Chat Display
│   ├── Message Input
│   └── Response Streaming
│
├── Sidebar
│   ├── API Config Panel
│   ├── PDF Uploader
│   └── Status Indicators
│
├── Session State
│   ├── Message History
│   ├── Agent Instance
│   └── PDF Status
│
└── Debug Panel
    ├── Query Type Display
    ├── Context Preview
    └── Error Messages
```

---

## 🔐 Security Architecture

```
┌─────────────────────────────────────┐
│        Security Layers               │
│                                      │
│  1. Environment Variables            │
│     • API keys in .env              │
│     • Never committed to git        │
│                                      │
│  2. Input Validation                 │
│     • Query sanitization            │
│     • File type checking            │
│     • Size limits                   │
│                                      │
│  3. Error Handling                   │
│     • No sensitive data in errors   │
│     • Graceful degradation          │
│     • Logging without secrets       │
│                                      │
│  4. API Security                     │
│     • Key rotation support          │
│     • Rate limiting ready           │
│     • Timeout configuration         │
└─────────────────────────────────────┘
```

---

## 📈 Scalability Considerations

### Current Architecture (Development)

```
Single Process
    │
    ├── In-Memory Qdrant
    ├── Synchronous Processing
    └── Local File Storage
```

### Production Architecture (Future)

```
Load Balancer
    │
    ├── App Server 1 ──┐
    ├── App Server 2 ──┼──→ Persistent Qdrant Cluster
    └── App Server N ──┘         │
                                  ├── S3 Document Storage
                                  └── Redis Cache Layer
```

---

## 🔍 Monitoring & Observability

```
┌────────────────────────────────────┐
│         LangSmith Layer             │
│                                     │
│  • Trace every LLM call            │
│  • Token usage tracking            │
│  • Latency monitoring              │
│  • Error rate analysis             │
└────────────────────────────────────┘
           │
           ▼
┌────────────────────────────────────┐
│       Application Logs              │
│                                     │
│  • Query routing decisions         │
│  • API call results                │
│  • Vector search metrics           │
│  • Error stack traces              │
└────────────────────────────────────┘
```

---

## 💾 Data Storage Architecture

### Vector Database Schema

```
Collection: "pdf_documents"
│
├── Vectors (1536-dim, COSINE)
│   └── Embeddings from OpenAI ada-002
│
└── Payload
    ├── page_content: str  (original text)
    ├── metadata: dict
    │   ├── source: str     (filename)
    │   ├── page: int       (page number)
    │   └── chunk_id: int   (chunk identifier)
    └── timestamp: datetime
```

### State Management

```
GraphState (TypedDict)
│
├── query: str              (user input)
├── query_type: Literal     ("weather" | "pdf" | "unknown")
├── weather_data: dict      (API response)
├── pdf_context: str        (retrieved chunks)
├── llm_response: str       (final answer)
└── error: str              (error messages)
```

---

## 🎯 Design Patterns Used

1. **State Machine Pattern**
   - LangGraph manages state transitions
   - Clear node definitions
   - Conditional routing

2. **Strategy Pattern**
   - Different handlers for query types
   - Pluggable processing strategies

3. **Singleton Pattern**
   - Single AI Agent instance
   - Shared vector store

4. **Observer Pattern**
   - LangSmith traces all events
   - Logging throughout pipeline

5. **Factory Pattern**
   - Dynamic prompt generation
   - Response formatting

---

This architecture provides:
- ✅ Clear separation of concerns
- ✅ Scalability potential
- ✅ Maintainability
- ✅ Testability
- ✅ Observability
- ✅ Security

Ready for production deployment with minimal modifications!