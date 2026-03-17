import sqlite3
from werkzeug.security import generate_password_hash

DATABASE_PATH = "inkwell.db"


def get_db():
    """Returns a SQLite connection with Row factory and foreign keys enabled."""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    """Creates all tables if they don't exist."""
    db = get_db()
    cursor = db.cursor()

    # users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            is_admin INTEGER DEFAULT 0,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # posts table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            slug TEXT UNIQUE NOT NULL,
            content TEXT NOT NULL,
            excerpt TEXT,
            status TEXT DEFAULT 'draft',
            author_id INTEGER NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (author_id) REFERENCES users(id)
        )
    """)

    # likes table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS likes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            post_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            FOREIGN KEY (post_id) REFERENCES posts(id),
            FOREIGN KEY (user_id) REFERENCES users(id),
            UNIQUE(post_id, user_id)
        )
    """)

    # saved_posts table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS saved_posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            post_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            saved_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (post_id) REFERENCES posts(id),
            FOREIGN KEY (user_id) REFERENCES users(id),
            UNIQUE(post_id, user_id)
        )
    """)

    db.commit()
    db.close()


def seed_db():
    """Inserts admin user and dummy posts if database is empty."""
    db = get_db()
    cursor = db.cursor()

    # Check if users already exist
    cursor.execute("SELECT COUNT(*) as count FROM users")
    if cursor.fetchone()["count"] > 0:
        db.close()
        return

    # Insert admin user
    admin_password_hash = generate_password_hash("admin123")
    cursor.execute(
        """
        INSERT INTO users (username, email, password_hash, is_admin)
        VALUES (?, ?, ?, ?)
        """,
        ("admin", "admin@inkwell.com", admin_password_hash, 1),
    )
    admin_id = cursor.lastrowid

    # Insert dummy posts
    dummy_posts = [
        {
            "title": "Getting Started with Python",
            "slug": "getting-started-with-python",
            "excerpt": "Python is one of the most beginner-friendly languages out there. Let's explore why.",
            "content": "<p>Python is one of the most beginner-friendly languages out there. It has a clean syntax, a massive community, and libraries for virtually everything.</p><p>In this post we'll look at how to get started from scratch.</p>",
        },
        {
            "title": "Understanding Flask Routing",
            "slug": "understanding-flask-routing",
            "excerpt": "Routing is the backbone of any Flask application. Here is how it works.",
            "content": "<p>Flask routing maps URLs to Python functions. Every time a user visits a URL, Flask figures out which function to call and returns its response.</p><p>Let's break down how this works under the hood.</p>",
        },
        {
            "title": "Why SQLite is Perfect for Small Projects",
            "slug": "why-sqlite-is-perfect-for-small-projects",
            "excerpt": "No server, no setup, no hassle. SQLite just works.",
            "content": "<p>SQLite is a file-based database that requires zero configuration. There is no server to run, no credentials to manage, and no installation beyond a Python package.</p><p>For small to medium projects, it is often the best choice.</p>",
        },
        {
            "title": "Async Programming in Python",
            "slug": "async-programming-in-python",
            "excerpt": "Master async/await to write fast, non-blocking code.",
            "content": "<p>Async programming allows you to write code that can handle multiple tasks without blocking. Learn how to use async/await in Python.</p><p>This is essential for building high-performance web applications.</p>",
        },
        {
            "title": "Database Design Best Practices",
            "slug": "database-design-best-practices",
            "excerpt": "Design robust databases that scale with your application.",
            "content": "<p>Good database design is crucial for application performance and maintainability. Learn the principles of normalization, indexing, and query optimization.</p><p>We'll explore practical patterns you can apply immediately.</p>",
        },
    ]

    for post in dummy_posts:
        cursor.execute(
            """
            INSERT INTO posts (title, slug, content, excerpt, status, author_id)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                post["title"],
                post["slug"],
                post["content"],
                post["excerpt"],
                "published",
                admin_id,
            ),
        )

    db.commit()
    db.close()
