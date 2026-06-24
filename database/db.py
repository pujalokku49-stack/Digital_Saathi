"""SQLite database connection and schema initialization."""
import sqlite3
from datetime import datetime

from werkzeug.security import generate_password_hash

from config import Config


def get_db():
    """Return a SQLite connection with row factory enabled."""
    conn = sqlite3.connect(Config.DATABASE)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def close_db(conn):
    """Close database connection."""
    if conn is not None:
        conn.close()


def init_db():
    """Create tables and seed default admin user if missing."""
    conn = get_db()
    cursor = conn.cursor()

    cursor.executescript(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            phone TEXT,
            preferred_language TEXT DEFAULT 'en',
            is_admin INTEGER DEFAULT 0,
            created_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS chat_queries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            query_text TEXT NOT NULL,
            response_text TEXT,
            language TEXT DEFAULT 'en',
            source TEXT DEFAULT 'chatbot',
            created_at TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE SET NULL
        );

        CREATE TABLE IF NOT EXISTS module_progress (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            module_name TEXT NOT NULL,
            lesson_id TEXT NOT NULL,
            completed INTEGER DEFAULT 0,
            updated_at TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
            UNIQUE(user_id, module_name, lesson_id)
        );
        """
    )

    # Seed default admin account (password: Admin@123)
    admin = cursor.execute(
        "SELECT id FROM users WHERE email = ?", ("admin@digitalsaathi.in",)
    ).fetchone()

    if admin is None:
        cursor.execute(
            """
            INSERT INTO users (name, email, password_hash, phone, preferred_language, is_admin, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                "System Admin",
                "admin@digitalsaathi.in",
                generate_password_hash("Admin@123"),
                "9999999999",
                "en",
                1,
                datetime.utcnow().isoformat(),
            ),
        )

    conn.commit()
    conn.close()
