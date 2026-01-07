# 🌦️📄 AI Agent – Weather & PDF RAG Pipeline

A **production-ready, test-driven AI agent** built using **LangChain, LangGraph, and LangSmith** that intelligently routes user queries between:

* **Real-time weather intelligence** 🌍
* **PDF-based document Q&A using RAG (Retrieval-Augmented Generation)** 📚

This project is designed to demonstrate **clean architecture, strong agent orchestration, observability, and reliability**, making it suitable for **interviews, assignments, and real-world GenAI systems**.

---

## 🚀 What This Agent Can Do

✅ Automatically understand *what the user is asking*

* Weather question → fetches **live weather data**
* Document question → queries **uploaded PDFs using RAG**

✅ Handles **errors gracefully** (missing PDFs, API failures, invalid queries)

✅ Fully **unit-tested** with deterministic behavior

✅ Includes **LangSmith tracing** for observability

✅ Comes with a **Streamlit UI** for interactive usage

---

## 🧠 High-Level Architecture

```
User (Streamlit UI)
        │
        ▼
┌────────────────────────────┐
│     LangGraph Pipeline     │
│                            │
│  ┌──────── Router ──────┐ │
│  │ Classifies the query │ │
│  └───────┬─────────────┘ │
│          │                │
│   ┌──────┴──────┐         │
│   ▼             ▼         │
│ Weather Node   PDF RAG Node│
│ (API Call)   (Vector Search)
│   │             │         │
│   └──────┬──────┘         │
│          ▼                │
│   LLM Response Generator  │
└────────────────────────────┘
        │
        ▼
Final Natural Language Answer
```

---

## 🧩 Core Design Principles

* **Single Responsibility Nodes** – Each node does one thing well
* **Deterministic Routing** – Predictable and testable logic
* **Fail-Safe PDF Handling** – Graceful fallback if PDF is missing
* **Mock-Friendly Design** – All external services are test-isolated
* **Production Logging** – Clear logs for debugging and tracing

---

## 📦 Project Structure

```
ai-agent-pipeline/
│
├── main.py          # Core agent + LangGraph pipeline
├── app.py           # Streamlit UI
├── test_main.py     # Unit & integration tests
├── requirements.txt
├── .env.example
├── README.md
└── sample_docs/     # Optional PDFs
```

---

## ⚙️ Installation & Setup

### 1️⃣ Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows
```

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Configure Environment Variables

Create a `.env` file:

```
OPENAI_API_KEY=your_openai_key
OPENWEATHER_API_KEY=your_weather_key
LANGSMITH_API_KEY=your_langsmith_key  # optional
```

---

## 🖥️ Running the Application

```bash
streamlit run app.py
```

Then open:

👉 **[http://localhost:8501](http://localhost:8501)**

---

## 💬 Example Queries

### 🌤️ Weather Queries

* "What’s the weather in Bangalore?"
* "Is it raining in London today?"
* "Temperature in New York"

### 📄 PDF Queries

1. Upload a PDF from the sidebar
2. Click **Load PDF**
3. Ask questions like:

* "What is this document about?"
* "Summarize section 2"
* "What does it say about security?"

---

## 📚 PDF RAG Workflow (Under the Hood)

1️⃣ Load PDF using **PyPDFLoader**

2️⃣ Split text into overlapping chunks

3️⃣ Generate embeddings using **OpenAI Embeddings**

4️⃣ Store vectors in **Qdrant (in-memory)**

5️⃣ Retrieve top relevant chunks at query time

6️⃣ Pass context to LLM for grounded answers

---

## 🌦️ Weather Pipeline

* Extract city from user query
* Call **OpenWeatherMap API**
* Normalize response
* Generate natural language summary via LLM

---

## 🧪 Testing Strategy

✔ Router logic
✔ Weather response generation
✔ PDF retrieval success & failure cases
✔ LLM response formatting
✔ End-to-end graph execution

Run tests:

```bash
pytest test_main.py -v
```

Coverage:

```bash
pytest --cov=main
```

---

## 📊 Observability with LangSmith

When enabled, LangSmith tracks:

* Prompt ↔ response traces
* Token usage
* Latency
* Error paths

Access dashboard:

👉 [https://smith.langchain.com](https://smith.langchain.com)

---

## 🔒 Security & Best Practices

* API keys via environment variables
* No secrets committed
* Sanitized error messages
* Mocked external calls in tests

---

## 🚧 Common Issues & Fixes

### ❌ PDF Not Loaded

✔ Agent returns a safe fallback message

### ❌ API Failure

✔ Logged error + user-friendly response

### ❌ Vector Store Empty

✔ No crash, clean degradation

---

## 🌱 Future Enhancements

* Multi-PDF support
* Persistent Qdrant storage
* Conversational memory
* Streaming responses
* Multi-tool agents

---

## 👤 Author

**Manish Saraswat**
AI / ML / GenAI Engineer

---

## ⭐ Final Notes

This project is intentionally built to reflect **real-world GenAI engineering standards**:

* Clean architecture
* Strong testing discipline
* Clear separation of concerns
* Interview-ready explanations

If you want:

* Code walkthroughs
* Interview Q&A prep
* Architecture diagrams
* Resume bullets

👉 Just ask 🚀

---

**Built with ❤️ using LangChain, LangGraph, Qdrant & Streamlit**
