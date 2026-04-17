import sqlite3
from werkzeug.security import generate_password_hash
from datetime import datetime

DATABASE = 'spendly.db'


def get_db():
    """Return SQLite connection with row_factory and foreign keys enabled."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    conn.execute('PRAGMA foreign_keys = ON')
    return conn


def init_db():
    """Create database tables if they don't exist."""
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        amount REAL NOT NULL,
        category TEXT NOT NULL,
        date TEXT NOT NULL,
        description TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )''')

    conn.commit()
    conn.close()


def seed_db():
    """Insert sample data if not already present."""
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute('SELECT COUNT(*) FROM users')
    if cursor.fetchone()[0] > 0:
        conn.close()
        return

    password_hash = generate_password_hash('demo123')
    cursor.execute('INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)',
                   ('Demo User', 'demo@spendly.com', password_hash))

    cursor.execute('SELECT id FROM users WHERE email = ?', ('demo@spendly.com',))
    user_id = cursor.fetchone()[0]

    today = datetime.now().strftime('%Y-%m-%d')
    expenses = [
        (user_id, 250.50, 'Food', today, 'Lunch at restaurant'),
        (user_id, 150.00, 'Transport', today, 'Uber ride'),
        (user_id, 1200.00, 'Bills', today, 'Electricity bill'),
        (user_id, 500.00, 'Health', today, 'Doctor visit'),
        (user_id, 800.00, 'Entertainment', today, 'Movie tickets'),
        (user_id, 2500.00, 'Shopping', today, 'New clothes'),
        (user_id, 300.00, 'Other', today, 'Miscellaneous'),
        (user_id, 450.75, 'Food', today, 'Grocery shopping'),
    ]

    cursor.executemany('INSERT INTO expenses (user_id, amount, category, date, description) VALUES (?, ?, ?, ?, ?)', expenses)

    conn.commit()
    conn.close()
