import sqlite3
import os
from datetime import datetime

DB_PATH = "db/prices.db"

def init_db():
    os.makedirs("db", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS prices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            datetime TEXT,
            url TEXT,
            title TEXT,
            price INTEGER
        )
    """)
    conn.commit()
    conn.close()

def insert_price(data: dict):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO prices (datetime, url, title, price)
        VALUES (?, ?, ?, ?)
    """, (
        datetime.now().isoformat(),
        data["url"],
        data["title"],
        data["price"]
    ))
    conn.commit()
    conn.close()
