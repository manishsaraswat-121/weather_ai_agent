# Detailed Setup Guide

This guide will walk you through setting up the AI Agent Pipeline from scratch.

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Getting API Keys](#getting-api-keys)
3. [Installation Steps](#installation-steps)
4. [Configuration](#configuration)
5. [Running the Application](#running-the-application)
6. [Testing](#testing)
7. [Troubleshooting](#troubleshooting)

## Prerequisites

### System Requirements

- **Operating System**: Windows 10+, macOS 10.14+, or Linux
- **Python**: Version 3.9 or higher
- **RAM**: Minimum 4GB (8GB recommended)
- **Disk Space**: At least 1GB free space

### Check Python Installation

```bash
# Check Python version
python --version
# or
python3 --version

# Should output: Python 3.9.x or higher
```

If Python is not installed:
- **Windows**: Download from [python.org](https://www.python.org/downloads/)
- **macOS**: Install via Homebrew: `brew install python@3.9`
- **Linux**: Use package manager: `sudo apt install python3.9`

## Getting API Keys

### 1. OpenAI API Key (Required)

1. Go to [OpenAI Platform](https://platform.openai.com/)
2. Sign up or log in
3. Navigate to **API Keys** section
4. Click **Create new secret key**
5. Copy the key (starts with `sk-...`)
6. **Important**: Save it securely; you won't see it again

**Cost**: ~$0.002 per 1000 tokens (very affordable for testing)

### 2. OpenWeather API Key (Required)

1. Go to [OpenWeatherMap](https://openweathermap.org/api)
2. Sign up for a free account
3. Navigate to **API Keys** section
4. Copy your default API key
5. **Note**: It may take a few minutes to activate

**Cost**: Free tier includes 1000 calls/day

### 3. LangSmith API Key (Optional)

1. Go to [LangSmith](https://smith.langchain.com/)
2. Sign up with your email
3. Navigate to **Settings** → **API Keys**
4. Click **Create API Key**
5. Copy the key

**Cost**: Free tier includes 5000 traces/month

## Installation Steps

### Step 1: Download the Project

If you have the zip file:
```bash
# Extract the zip file
unzip ai-agent-pipeline.zip
cd ai-agent-pipeline
```

Or clone from GitHub:
```bash
git clone <your-repo-url>
cd ai-agent-pipeline
```

### Step 2: Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt.

### Step 3: Install Dependencies

```bash
# Upgrade pip first
pip install --upgrade pip

# Install all requirements
pip install -r requirements.txt
```

This will install approximately 50+ packages. It may take 2-5 minutes.

### Step 4: Verify Installation

```bash
# Check if key packages are installed
python -c "import langchain; import streamlit; import qdrant_client; print('✅ All imports successful')"
```

## Configuration

### Step 1: Create Environment File

```bash
# Copy the example file
cp .env.example .env

# On Windows:
copy .env.example .env
```

### Step 2: Edit .env File

Open `.env` in any text editor and add your keys:

```bash
# Required
OPENAI_API_KEY=sk-your-openai-key-here
OPENWEATHER_API_KEY=your-openweather-key-here

# Optional (for LangSmith tracking)
LANGSMITH_API_KEY=your-langsmith-key-here
LANGCHAIN_PROJECT=weather-pdf-rag-agent
LANGCHAIN_TRACING_V2=true
```

**Important**: 
- Don't add quotes around the keys
- Don't add spaces around the `=` sign
- Keep the `.env` file secret (it's in `.gitignore`)

### Step 3: Verify Configuration

```bash
# Test if environment variables load correctly
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print('OpenAI:', 'Configured' if os.getenv('OPENAI_API_KEY') else 'Missing')"
```

## Running the Application

### Option 1: Use Quick Start Scripts

**Linux/macOS:**
```bash
chmod +x run.sh
./run.sh
```

**Windows:**
```bash
run.bat
```

### Option 2: Manual Start

**Start Streamlit UI:**
```bash
streamlit run app.py
```

The app will open at: `http://localhost:8501`

**Run Tests:**
```bash
python -m pytest test_main.py -v
```

## Testing

### Run All Tests

```bash
# Basic test run
python -m pytest test_main.py -v

# With coverage report
python -m pytest test_main.py --cov=main --cov-report=html

# Open coverage report
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
start htmlcov/index.html  # Windows
```

### Run Specific Tests

```bash
# Test routing
python -m pytest test_main.py::TestAIAgent::test_route_query_weather -v

# Test weather API
python -m pytest test_main.py::TestAIAgent::test_fetch_weather_success -v

# Test PDF processing
python -m pytest test_main.py::TestAIAgent::test_load_pdf_success -v
```

## Using the Application

### 1. First Time Setup in UI

1. Open the app at `http://localhost:8501`
2. Click the sidebar **Configuration** section
3. Enter your API keys (if not in .env)
4. Click **Save Configuration**
5. You should see "✅ Agent initialized successfully!"

### 2. Testing Weather Queries

Try these example queries:
- "What's the weather in London?"
- "Tell me the temperature in Tokyo"
- "Is it sunny in New York?"

### 3. Testing PDF Queries

1. **Upload a PDF**:
   - Click **Browse files** in the sidebar
   - Select any PDF document
   - Click **Load PDF**
   - Wait for "✅ PDF loaded successfully!"

2. **Query the PDF**:
   - "What is this document about?"
   - "Summarize the main points"
   - "Tell me about [specific topic]"

### 4. Viewing Debug Information

- After each response, expand **🔍 Debug Info**
- See query routing decisions
- View retrieved context
- Check for errors

## LangSmith Setup (Optional)

### 1. Enable Tracking

If you've configured `LANGSMITH_API_KEY` in `.env`:

```bash
# Environment variables (already in .env)
LANGSMITH_API_KEY=your-key
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT=weather-pdf-rag-agent
```

### 2. View Traces

1. Go to [smith.langchain.com](https://smith.langchain.com/)
2. Select project: **weather-pdf-rag-agent**
3. View traces for each query
4. Analyze performance metrics

### 3. Taking Screenshots

For the assignment:
1. Run a few queries
2. Go to LangSmith dashboard
3. Take screenshots of:
   - Project overview
   - Individual trace details
   - Token usage metrics
   - Error rates (if any)

## Troubleshooting

### Issue: "Module not found" errors

**Solution:**
```bash
# Make sure virtual environment is activated
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate  # Windows

# Reinstall requirements
pip install -r requirements.txt --force-reinstall
```

### Issue: "Invalid API key"

**Solution:**
1. Check `.env` file for correct keys
2. Verify no extra spaces or quotes
3. Test keys individually:

```bash
# Test OpenAI key
python -c "from openai import OpenAI; client = OpenAI(); print('✅ OpenAI key valid')"

# Test OpenWeather key
curl "http://api.openweathermap.org/data/2.5/weather?q=London&appid=YOUR_KEY"
```

### Issue: Streamlit won't start

**Solution:**
```bash
# Kill any existing Streamlit processes
pkill -f streamlit  # Linux/macOS
taskkill /F /IM streamlit.exe  # Windows

# Try different port
streamlit run app.py --server.port 8502
```

### Issue: PDF won't load

**Solution:**
1. Ensure PDF is not encrypted or password-protected
2. Try a different PDF
3. Check file size (very large PDFs may take time)
4. Look for errors in terminal

### Issue: Tests failing

**Solution:**
```bash
# Update pytest
pip install --upgrade pytest pytest-cov

# Run with more verbose output
python -m pytest test_main.py -vv --tb=short

# Skip specific tests if needed
python -m pytest test_main.py -k "not test_load_pdf"
```

### Issue: "Rate limit exceeded"

**Solution:**
- OpenAI: You've exceeded your quota. Check billing.
- OpenWeather: Wait a minute (60 calls/minute limit on free tier)

## Performance Tips

1. **For faster PDF processing**:
   - Use smaller PDFs during testing
   - Reduce chunk_size in `main.py` if needed

2. **For better responses**:
   - Use GPT-4 instead of GPT-3.5 (costs more)
   - Increase retrieval chunks (`k=5` instead of `k=3`)

3. **For production**:
   - Use persistent Qdrant storage
   - Implement caching
   - Add rate limiting

## Next Steps

1. ✅ Complete setup
2. ✅ Run tests successfully
3. ✅ Test with weather queries
4. ✅ Upload and query a PDF
5. ✅ Capture LangSmith screenshots
6. ✅ Record Loom video
7. ✅ Push to GitHub
8. ✅ Submit assignment

## Getting Help

If you're still stuck:
1. Check the main README.md
2. Review test output for specific errors
3. Look at console logs in terminal
4. Check LangSmith for LLM errors

## Useful Commands Cheat Sheet

```bash
# Activate environment
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate  # Windows

# Run application
streamlit run app.py

# Run tests
python -m pytest test_main.py -v

# Run with coverage
python -m pytest test_main.py --cov=main --cov-report=html

# Check imports
python -c "import langchain, streamlit, qdrant_client; print('OK')"

# Update packages
pip install -r requirements.txt --upgrade

# Deactivate environment
deactivate
```

---

**Good luck with your assignment! 🚀**