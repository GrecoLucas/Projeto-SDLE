"""
Shopping List Application - Tkinter Version
Local-First Shopping List with Tkinter Interface
"""
from src import db
from src.Ui.ui_tk import start_ui
import sys


def main():
    """Initialize database and start Tkinter GUI.
    Usage:
      python3 main_tk.py        # use existing DB
      python3 main_tk.py db     # recreate DB
    """

    if len(sys.argv) > 1 and sys.argv[1] == "db":
        db.destroy_db()
        db.init_db()
        print("New database initialized.")
    
    print("Using old database.")
    for i in db.get_all_users():
        print(f"User: {i}")

    start_ui()


if __name__ == "__main__":
    main()
