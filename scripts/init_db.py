#!/usr/bin/env python3
"""
Helper script to initialize or reset the database.
Usage:
    python scripts/init_db.py          # Initialize if not exists
    python scripts/init_db.py --force  # Force recreate database
"""

import sys
from pathlib import Path

# Add parent directory to path to import src
sys.path.insert(0, str(Path(__file__).parent.parent))

from src import db

def main():
    force = "--force" in sys.argv or "-f" in sys.argv
    
    if force:
        print("Destroying existing database...")
        db.destroy_db()
    
    print("Initializing database...")
    try:
        db.init_db()
        print("Database initialized successfully!")
        print(f"Database location: {db.DB_PATH}")
    except Exception as e:
        print(f"Error initializing database: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
