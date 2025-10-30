"""
Shopping List Application - Tkinter Version
Local-First Shopping List with Tkinter Interface
"""
from src import db
from src.Ui.ui_tk import start_ui


def main():
    """Initialize database and start Tkinter GUI"""
    #db.init_db()
    start_ui()


if __name__ == "__main__":
    main()
