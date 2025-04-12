import sqlite3
import os
from datetime import datetime, timedelta
import random

def initialize_database():
    # Create data directory if it doesn't exist
    os.makedirs("data", exist_ok=True)
    
    # Connect to SQLite database (creates it if it doesn't exist)
    conn = sqlite3.connect("data/expenses.db")
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT,
            password TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Create expenses table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            description TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    """)
    
    # Create indexes for better performance
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_expenses_user ON expenses (user_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_expenses_date ON expenses (date)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_expenses_category ON expenses (category)")
    
    # Add a test user if none exists (for demo purposes)
    cursor.execute("SELECT id FROM users WHERE username = 'testuser'")
    if not cursor.fetchone():
        cursor.execute(
            "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
            ("testuser", "test@example.com", "test123")
        )
        user_id = cursor.lastrowid
        
        # Add some sample expenses
        categories = ["Food", "Transport", "Housing", "Entertainment", "Utilities"]
        today = datetime.now().date()
        
        for i in range(30):
            date = (today - timedelta(days=i)).strftime("%Y-%m-%d")
            for _ in range(random.randint(1, 4)):
                category = random.choice(categories)
                amount = round(random.uniform(5, 100), 2)
                cursor.execute(
                    "INSERT INTO expenses (user_id, date, category, amount, description) VALUES (?, ?, ?, ?, ?)",
                    (user_id, date, category, amount, f"Sample expense {i}")
                )
    
    conn.commit()
    conn.close()
    print("Database initialized successfully!")

if __name__ == "__main__":
    initialize_database()