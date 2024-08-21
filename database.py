import sqlite3 as sql

db = sql.connect("database.db", check_same_thread=False)
cursor = db.cursor()

cursor.executescript(
    """
    DROP TABLE IF EXISTS message;
    DROP TABLE IF EXISTS user;

    CREATE TABLE IF NOT EXISTS user (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        first_name VARCHAR(65),
        username VARCHAR(65)
    );

    CREATE TABLE IF NOT EXISTS message (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        message_id INTEGER,
        content TEXT,
        translated_content TEXT,
        user_id INTEGER
    );
""")