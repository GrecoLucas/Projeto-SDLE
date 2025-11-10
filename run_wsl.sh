#!/bin/bash
# Quick setup and run script for WSL
# Usage: ./run_wsl.sh

set -e  # Exit on error

echo "🚀 Projeto SDLE - WSL Setup & Run"
echo "=================================="

# Check if python3-tk is installed
if ! python3 -c "import tkinter" 2>/dev/null; then
    echo "⚠️  python3-tk not found. Installing..."
    sudo apt update
    sudo apt install -y python3-tk python3-venv
fi

# Create venv if not exists
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate venv
echo "🔌 Activating virtual environment..."
source .venv/bin/activate

# Initialize DB if not exists
if [ ! -f "data/db.sqlite" ]; then
    echo "🗄️  Initializing database..."
    python -c "from src import db; db.init_db()"
fi

# Check DISPLAY
if [ -z "$DISPLAY" ]; then
    echo "⚠️  DISPLAY not set. Setting for WSLg/VcXsrv..."
    export DISPLAY=:0
fi

echo "✅ Setup complete!"
echo "🎨 Launching GUI..."
python main_tk.py
