#!/bin/bash
# Simple run script for Linux/Mac/WSL
# Usage: ./run.sh

# Initialize database if it doesn't exist
if [ ! -f "data/db.sqlite" ]; then
    echo "Creating database..."
    python3 -c "from src import db; db.init_db()"
fi

# Run the application
echo "Starting Shopping List application..."
python3 main_tk.py
