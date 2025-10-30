"""
Shopping List Application - GUI Version
Local-First Shopping List with Dear PyGui Interface
"""
from src import db
from src.Ui.ui import start_ui


def main():
    """Initialize database and start GUI"""
    # Initialize database
    db.init_db()
    
    # Start the Dear PyGui interface
    start_ui()


if __name__ == '__main__':
    main()
