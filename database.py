import sqlite3
import os
from config import Config

def get_db_connection():
    os.makedirs(os.path.dirname(Config.DATABASE_PATH), exist_ok=True)
    conn = sqlite3.connect(Config.DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # User Account Table Layout
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Analysis History Audit Tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS analysis_history (
            analysis_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            job_title TEXT NOT NULL,
            ats_score INTEGER NOT NULL,
            skills_found TEXT NOT NULL,
            missing_skills TEXT NOT NULL,
            suggestions TEXT NOT NULL,
            summary TEXT NOT NULL,
            analyzed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (user_id)
        )
    ''')
    
    # Seed default sandbox profile record if empty
    cursor.execute("INSERT OR IGNORE INTO users (user_id, email) VALUES (1, 'student@csbs.edu')")
    conn.commit()
    conn.close()