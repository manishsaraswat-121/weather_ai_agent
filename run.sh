#!/bin/bash

# AI Agent Pipeline - Quick Start Script
# This script sets up and runs the application

echo "🚀 AI Agent Pipeline - Quick Start"
echo "=================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.9 or higher."
    exit 1
fi

echo "✅ Python found: $(python3 --version)"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi
echo ""

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate
echo ""

# Install dependencies
echo "📚 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
echo "✅ Dependencies installed"
echo ""

# Check for .env file
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found!"
    echo "📝 Creating .env from template..."
    cp .env.example .env
    echo ""
    echo "⚠️  IMPORTANT: Please edit .env and add your API keys:"
    echo "   - OPENAI_API_KEY"
    echo "   - OPENWEATHER_API_KEY"
    echo "   - LANGSMITH_API_KEY (optional)"
    echo ""
    echo "Press Enter after you've updated the .env file..."
    read
fi

# Load environment variables
if [ -f ".env" ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

# Check if API keys are set
if [ -z "$OPENAI_API_KEY" ] || [ -z "$OPENWEATHER_API_KEY" ]; then
    echo "❌ API keys not configured in .env file"
    echo "Please set OPENAI_API_KEY and OPENWEATHER_API_KEY"
    exit 1
fi

echo "✅ API keys configured"
echo ""

# Ask user what to run
echo "What would you like to do?"
echo "1) Run Streamlit UI (Recommended)"
echo "2) Run Tests"
echo "3) Both"
echo ""
read -p "Enter choice (1-3): " choice

case $choice in
    1)
        echo ""
        echo "🎨 Starting Streamlit UI..."
        echo "Open your browser at http://localhost:8501"
        echo ""
        streamlit run app.py
        ;;
    2)
        echo ""
        echo "🧪 Running tests..."
        python -m pytest test_main.py -v --cov=main --cov-report=term-missing
        ;;
    3)
        echo ""
        echo "🧪 Running tests first..."
        python -m pytest test_main.py -v
        echo ""
        echo "✅ Tests completed"
        echo ""
        echo "🎨 Starting Streamlit UI..."
        echo "Open your browser at http://localhost:8501"
        echo ""
        streamlit run app.py
        ;;
    *)
        echo "❌ Invalid choice"
        exit 1
        ;;
esac