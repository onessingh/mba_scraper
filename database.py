import sqlite3
import os

class ScraperDatabase:
    def __init__(self, db_path=None):
        if db_path is None:
            # Use notices.db inside the mba_scraper folder
            base_dir = os.path.dirname(os.path.abspath(__file__))
            self.db_path = os.path.join(base_dir, 'notices.db')
        else:
            self.db_path = db_path
        self._init_db()

    def _init_db(self):
        """Initialize the database and create the notices table if it doesn't exist."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS notices (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    link TEXT,
                    title TEXT,
                    semester TEXT,
                    processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    is_deleted INTEGER DEFAULT 0,
                    UNIQUE(link, title)
                )
            ''')
            conn.commit()

    def is_link_new(self, link, title):
        """Check if a link+title combination already exists in the database."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT 1 FROM notices WHERE link = ? AND title = ?', (link, title))
            return cursor.fetchone() is None

    def save_link(self, link, title, semester):
        """Store a new link in the database."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    'INSERT INTO notices (link, title, semester) VALUES (?, ?, ?)',
                    (link, title, semester)
                )
                conn.commit()
                return True
        except sqlite3.IntegrityError:
            return False
