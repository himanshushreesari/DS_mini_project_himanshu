#!/bin/bash

# Quick Start Script for Population Deposits Dashboard
# This script sets up and launches the Streamlit dashboard

echo "========================================="
echo "Population Deposits Analysis Dashboard"
echo "========================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.11 or higher."
    exit 1
fi

echo "✅ Python found: $(python3 --version)"
echo ""

# Check if we're in the right directory
if [ ! -f "app.py" ]; then
    echo "❌ Error: app.py not found. Please run this script from the streamlit_app directory."
    exit 1
fi

echo "✅ Located in correct directory"
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
echo "✅ Virtual environment activated"
echo ""

# Install/upgrade pip
echo "📦 Upgrading pip..."
pip install --upgrade pip --quiet
echo "✅ Pip upgraded"
echo ""

# Install requirements
echo "📦 Installing required packages..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt --quiet
    echo "✅ All packages installed"
else
    echo "❌ requirements.txt not found!"
    exit 1
fi
echo ""

# Check if data files exist
echo "🔍 Checking for data files..."
DATA_DIR="../data/processed"
if [ -d "$DATA_DIR" ]; then
    if [ -f "$DATA_DIR/cleaned_data.csv" ] && [ -f "$DATA_DIR/featured_data.csv" ]; then
        echo "✅ Data files found"
    else
        echo "⚠️  Warning: Some data files may be missing in $DATA_DIR"
        echo "   The dashboard may not display all features correctly."
    fi
else
    echo "⚠️  Warning: Data directory not found at $DATA_DIR"
    echo "   Please ensure the project structure is correct."
fi
echo ""

# Check if model files exist
echo "🔍 Checking for model files..."
MODEL_DIR="../models/saved_models"
if [ -d "$MODEL_DIR" ]; then
    model_count=$(ls -1 "$MODEL_DIR"/*.pkl 2>/dev/null | wc -l)
    if [ $model_count -gt 0 ]; then
        echo "✅ Found $model_count model file(s)"
    else
        echo "⚠️  Warning: No model files found in $MODEL_DIR"
    fi
else
    echo "⚠️  Warning: Model directory not found at $MODEL_DIR"
fi
echo ""

# Launch Streamlit
echo "========================================="
echo "🚀 Launching Streamlit Dashboard..."
echo "========================================="
echo ""
echo "The dashboard will open in your browser at:"
echo "👉 http://localhost:8501"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

streamlit run app.py
