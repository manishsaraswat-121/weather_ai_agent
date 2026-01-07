# How to Use This Complete Project

## 📥 Step 1: Get All Files

I've created **12 complete files** for you in the artifacts. Here's how to save them:

### Files to Download:

1. **Core Python Files**:
   - `main.py` - The LangGraph pipeline (core logic)
   - `app.py` - Streamlit UI
   - `test_main.py` - Unit tests

2. **Configuration Files**:
   - `requirements.txt` - Python dependencies
   - `.env.example` - Environment template
   - `.gitignore` - Git ignore rules

3. **Documentation**:
   - `README.md` - Main documentation
   - `SETUP_GUIDE.md` - Detailed setup
   - `QUICK_REFERENCE.md` - Quick commands
   - `PROJECT_SUMMARY.md` - Technical overview
   - `SUBMISSION_CHECKLIST.md` - Pre-submission guide
   - `HOW_TO_USE_THIS_PROJECT.md` - This file

4. **Scripts**:
   - `run.sh` - Quick start (Linux/Mac)
   - `run.bat` - Quick start (Windows)
   - `create_package.py` - Package creator

5. **CI/CD**:
   - `.github/workflows/tests.yml` - GitHub Actions

### How to Save Files from Claude:

For each artifact above, click on it and:
1. Copy the content
2. Create a new file with the exact name shown
3. Paste the content
4. Save the file

---

## 📁 Step 2: Create Project Structure

Create this exact folder structure:

```
ai-agent-pipeline/
├── main.py
├── app.py
├── test_main.py
├── requirements.txt
├── .env.example
├── .env                    ← You'll create this
├── .gitignore
├── README.md
├── SETUP_GUIDE.md
├── QUICK_REFERENCE.md
├── PROJECT_SUMMARY.md
├── SUBMISSION_CHECKLIST.md
├── HOW_TO_USE_THIS_PROJECT.md
├── run.sh
├── run.bat
├── create_package.py
├── .github/
│   └── workflows/
│       └── tests.yml
├── sample_docs/            ← Create empty folder
├── langsmith_screenshots/  ← Create empty folder
└── tests/                  ← Create empty folder
    └── __init__.py         ← Create empty file
```

### Quick Setup Commands:

```bash
# Create main directory
mkdir ai-agent-pipeline
cd ai-agent-pipeline

# Create subdirectories
mkdir -p .github/workflows
mkdir sample_docs
mkdir langsmith_screenshots
mkdir tests

# Create __init__.py
touch tests/__init__.py

# Now copy all the files into this structure
```

---

## 🔧 Step 3: Install and Configure

### A. Create Virtual Environment

```bash
# Create venv
python3 -m venv venv

# Activate it
# On Mac/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### B. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

This will install approximately 50 packages (2-5 minutes).

### C. Get API Keys

You need these three API keys:

1. **OpenAI** (Required)
   - Go to: https://platform.openai.com/api-keys
   - Create account
   - Generate new API key
   - Copy it (starts with `sk-...`)

2. **OpenWeather** (Required)
   - Go to: https://openweathermap.org/api
   - Sign up for free account
   - Get your API key from dashboard
   - Free tier: 1000 calls/day

3. **LangSmith** (Optional but recommended)
   - Go to: https://smith.langchain.com/
   - Sign up
   - Settings → API Keys
   - Create new key
   - Free tier: 5000 traces/month

### D. Configure .env File

```bash
# Copy template
cp .env.example .env

# Edit .env and add your keys
nano .env  # or use any text editor
```

Your `.env` should look like:
```bash
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxx
OPENWEATHER_API_KEY=xxxxxxxxxxxxx
LANGSMITH_API_KEY=lsv2_pt_xxxxxxxxxxxxx
LANGCHAIN_PROJECT=weather-pdf-rag-agent
LANGCHAIN_TRACING_V2=true
```

---

## 🚀 Step 4: Run the Application

### Option 1: Use Quick Start Scripts

**Mac/Linux:**
```bash
chmod +x run.sh
./run.sh
```

**Windows:**
```bash
run.bat
```

Select option 1 (Run Streamlit UI).

### Option 2: Manual Start

```bash
# Make sure venv is activated
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows

# Run Streamlit
streamlit run app.py
```

The app will open at: http://localhost:8501

---

## 🧪 Step 5: Test the Application

### Run Unit Tests

```bash
# All tests
python -m pytest test_main.py -v

# With coverage
python -m pytest test_main.py --cov=main --cov-report=html

# Open coverage report
open htmlcov/index.html
```

### Manual Testing

1. **Test Weather Queries**:
   - Open app at http://localhost:8501
   - Ask: "What's the weather in London?"
   - Should get current weather data

2. **Test PDF Queries**:
   - Upload a PDF in sidebar
   - Click "Load PDF"
   - Ask: "What is this document about?"
   - Should get answer from PDF

---

## 📸 Step 6: Capture LangSmith Screenshots

If you configured LangSmith:

1. Run several queries (both weather and PDF)
2. Go to https://smith.langchain.com/
3. Select your project: "weather-pdf-rag-agent"
4. Take screenshots of:
   - Project dashboard
   - A weather query trace
   - A PDF query trace
   - Token usage metrics
   - Performance graphs

5. Save screenshots to `langsmith_screenshots/` folder

---

## 🎥 Step 7: Record Loom Video

Record a 5-10 minute video covering:

### Video Structure:

1. **Introduction** (30 seconds)
   - Your name
   - Project overview

2. **LangSmith Demo** (2-3 minutes)
   - Show dashboard
   - Walk through a trace
   - Explain metrics

3. **Code Walkthrough** (3-5 minutes)
   - Show `main.py` structure
   - Explain routing logic
   - Show RAG implementation
   - Explain vector database usage

4. **Live Demo** (2-3 minutes)
   - Run Streamlit app
   - Show weather query
   - Show PDF query
   - Explain results

5. **Testing** (1 minute)
   - Show test execution
   - Explain test coverage

### Recording Tips:
- Use clear audio
- Show code and UI side by side
- Zoom in on important parts
- Keep it concise

---

## 📦 Step 8: Create Submission Package

### Option 1: Use Package Script

```bash
python create_package.py
```

This creates `ai-agent-pipeline.zip` ready for submission.

### Option 2: Manual Zip

```bash
# From parent directory
zip -r ai-agent-pipeline.zip ai-agent-pipeline/ \
  -x "ai-agent-pipeline/venv/*" \
  -x "ai-agent-pipeline/.env" \
  -x "ai-agent-pipeline/__pycache__/*" \
  -x "ai-agent-pipeline/*.pyc"
```

---

## 🐙 Step 9: Push to GitHub

### Initialize Repository

```bash
cd ai-agent-pipeline

# Initialize git
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: AI Agent Pipeline"

# Create repo on GitHub and push
git remote add origin <your-repo-url>
git branch -M main
git push -u origin main
```

### Important: Verify .gitignore

Make sure these are NOT in your repo:
- `.env` file (contains secrets)
- `venv/` directory
- `__pycache__/` directories
- `*.pyc` files

---

## ✅ Step 10: Final Checklist

Use `SUBMISSION_CHECKLIST.md` to verify everything:

- [ ] All code files complete and working
- [ ] Tests pass successfully  
- [ ] Weather queries work
- [ ] PDF queries work
- [ ] LangSmith screenshots captured
- [ ] Loom video recorded
- [ ] GitHub repository created
- [ ] README.md is complete
- [ ] .env not committed to GitHub

---

## 🎯 Step 11: Submit

Your submission should include:

1. **GitHub Repository URL**
   - Contains all code
   - Has good README
   - Includes screenshots

2. **Loom Video Link**
   - 5-10 minutes
   - Covers code and demo
   - Public or unlisted

3. **Additional Files** (if required)
   - Test results
   - Coverage reports
   - Screenshots

---

## 🆘 Troubleshooting

### Common Issues:

**"Module not found" errors**
```bash
pip install -r requirements.txt --force-reinstall
```

**"Invalid API key"**
- Double-check .env file
- No spaces around = sign
- No quotes around keys
- Keys are complete

**"Streamlit won't start"**
```bash
# Try different port
streamlit run app.py --server.port 8502
```

**"Tests failing"**
```bash
# Check Python version
python --version  # Should be 3.9+

# Reinstall dependencies
pip install -r requirements.txt
```

**"PDF won't load"**
- Ensure PDF is not encrypted
- Try smaller PDF first
- Check file path is correct

---

## 📚 Additional Resources

### Documentation:
- Main README: `README.md`
- Setup Guide: `SETUP_GUIDE.md`
- Quick Reference: `QUICK_REFERENCE.md`
- Technical Details: `PROJECT_SUMMARY.md`

### External Links:
- [LangChain Docs](https://python.langchain.com/)
- [LangGraph Tutorial](https://langchain-ai.github.io/langgraph/)
- [LangSmith Guide](https://docs.smith.langchain.com/)
- [Streamlit Docs](https://docs.streamlit.io/)

---

## 🎉 You're Ready!

Follow these steps in order, and you'll have a complete, working AI Agent pipeline ready for submission.

**Estimated Time**:
- Setup: 30 minutes
- Testing: 15 minutes
- Screenshots: 10 minutes
- Video: 30 minutes
- GitHub: 15 minutes
- **Total: ~2 hours**

Good luck with your assignment! 🚀

---

## 💡 Pro Tips

1. **Test incrementally** - Don't wait until the end
2. **Read error messages carefully** - They usually tell you what's wrong
3. **Use the Quick Reference** - Keep it open while working
4. **Ask for help** - If stuck for >30 minutes, reach out
5. **Document as you go** - Take notes for your video

---

**Need help?** Review the documentation files or check the troubleshooting section.