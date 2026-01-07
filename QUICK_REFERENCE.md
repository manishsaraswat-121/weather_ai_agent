# Quick Reference Guide

## 🚀 Getting Started (3 Minutes)

```bash
# 1. Extract the zip
unzip ai-agent-pipeline.zip
cd ai-agent-pipeline

# 2. Create environment
python3 -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure API keys
cp .env.example .env
# Edit .env and add your keys

# 5. Run the app
streamlit run app.py
```

## 🔑 API Keys Required

| Service | Required? | Get From | Free Tier |
|---------|-----------|----------|-----------|
| OpenAI | ✅ Yes | https://platform.openai.com | $5 free credit |
| OpenWeather | ✅ Yes | https://openweathermap.org | 1000 calls/day |
| LangSmith | ⚠️ Optional | https://smith.langchain.com | 5000 traces/month |

## 📁 Project Structure

```
ai-agent-pipeline/
├── main.py              # 🧠 Core AI pipeline (LangGraph)
├── app.py               # 🎨 Streamlit UI
├── test_main.py         # 🧪 Unit tests
├── requirements.txt     # 📦 Dependencies
└── .env                 # 🔑 API keys (create from .env.example)
```

## 🎯 Key Commands

### Run Application
```bash
streamlit run app.py
```

### Run Tests
```bash
# All tests
pytest test_main.py -v

# With coverage
pytest test_main.py --cov=main --cov-report=html

# Specific test
pytest test_main.py::TestAIAgent::test_route_query_weather -v
```

### Quick Scripts
```bash
# Linux/Mac
./run.sh

# Windows
run.bat
```

## 💬 Example Queries

### Weather Queries
```
"What's the weather in London?"
"Tell me the temperature in Tokyo"
"Is it raining in Paris?"
"How's the weather in New York today?"
```

### PDF Queries (after uploading a PDF)
```
"What is this document about?"
"Summarize the main points"
"What does it say about [topic]?"
"List the key findings"
```

## 🏗️ Architecture Overview

```
User Query
    ↓
[Router Node] ← Decides: Weather or PDF?
    ↓
    ├─→ [Weather Node] → OpenWeatherMap API
    │
    └─→ [PDF RAG Node] → Qdrant Vector DB
            ↓
    [LLM Response Generator] ← GPT-3.5-turbo
            ↓
        Response
```

## 🧪 Testing Checklist

- [ ] Import test: `python -c "import langchain, streamlit; print('OK')"`
- [ ] Unit tests: `pytest test_main.py`
- [ ] Weather query: Ask about weather in any city
- [ ] PDF upload: Upload and query a document
- [ ] Error handling: Try invalid inputs
- [ ] LangSmith: Check traces at smith.langchain.com

## 🐛 Common Issues & Fixes

### "Module not found"
```bash
pip install -r requirements.txt --force-reinstall
```

### "Invalid API key"
```bash
# Check .env file has correct keys with no spaces
cat .env
```

### "Streamlit not starting"
```bash
# Try different port
streamlit run app.py --server.port 8502
```

### "PDF won't load"
- Ensure PDF is not encrypted
- Try a smaller PDF first
- Check terminal for errors

## 📊 LangSmith Setup

1. Add to `.env`:
```bash
LANGSMITH_API_KEY=your_key
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT=weather-pdf-rag-agent
```

2. View traces at: https://smith.langchain.com/

3. Screenshots needed:
   - Project dashboard
   - Weather query trace
   - PDF query trace
   - Token metrics

## 🎥 Loom Video Checklist

Cover these points (5-10 minutes):
- [ ] LangSmith dashboard tour
- [ ] Show traces for both query types
- [ ] Explain routing logic in code
- [ ] Walk through RAG implementation
- [ ] Show vector database usage
- [ ] Demo Streamlit UI
- [ ] Run and explain tests

## 📦 Code Components

### Main Pipeline (`main.py`)
- `AIAgent` class: Main orchestrator
- `route_query()`: Decides query type
- `fetch_weather()`: Gets weather data
- `fetch_pdf_context()`: RAG retrieval
- `generate_response()`: LLM response
- `load_pdf()`: Process & index PDFs

### UI (`app.py`)
- Chat interface
- API key configuration
- PDF upload handler
- Status indicators
- Debug information display

### Tests (`test_main.py`)
- Agent initialization
- Query routing
- API integration
- PDF processing
- Response generation
- Error handling

## 🔄 Development Workflow

1. **Start Development**
   ```bash
   source venv/bin/activate
   ```

2. **Make Changes**
   - Edit code
   - Test manually
   - Run unit tests

3. **Test**
   ```bash
   pytest test_main.py -v
   ```

4. **Run App**
   ```bash
   streamlit run app.py
   ```

5. **Commit**
   ```bash
   git add .
   git commit -m "Description"
   git push
   ```

## 📈 Performance Tips

- Use smaller PDFs during development
- GPT-4 gives better responses (costs more)
- Increase `k=5` in retriever for more context
- Use persistent Qdrant for production

## 🎓 Learning Resources

- [LangChain Docs](https://python.langchain.com/)
- [LangGraph Tutorial](https://langchain-ai.github.io/langgraph/)
- [LangSmith Guide](https://docs.smith.langchain.com/)
- [Qdrant Docs](https://qdrant.tech/documentation/)
- [Streamlit Docs](https://docs.streamlit.io/)

## ✅ Pre-Submission Checklist

- [ ] All tests pass
- [ ] Weather queries work
- [ ] PDF queries work
- [ ] LangSmith tracking enabled
- [ ] Screenshots captured
- [ ] Loom video recorded
- [ ] GitHub repo updated
- [ ] README is complete

## 🆘 Need Help?

1. Check `SETUP_GUIDE.md` for detailed instructions
2. Review `README.md` for comprehensive docs
3. Check test output for specific errors
4. Review LangSmith traces for LLM issues
5. Check terminal logs for runtime errors

## 📞 Support Resources

- LangChain Discord: https://discord.gg/langchain
- GitHub Issues: Create issue in your repo
- Stack Overflow: Tag with `langchain`, `langgraph`

---

**Quick tip**: Keep this guide open while developing! 💡