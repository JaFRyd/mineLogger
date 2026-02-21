import sqlite3
from pathlib import Path
from datetime import datetime, date

DB_DIR = Path.home() / ".minelogger"
DB_PATH = DB_DIR / "minelogger.db"


def _connect():
    DB_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with _connect() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS entries (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                date        TEXT    NOT NULL,
                customer    TEXT    NOT NULL,
                hours       REAL    NOT NULL,
                description TEXT    NOT NULL,
                created_at  TEXT    NOT NULL
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS customers (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                name       TEXT    NOT NULL UNIQUE,
                created_at TEXT    NOT NULL
            )
        """)


def add_entry(date_str, customer, hours, description):
    created_at = datetime.now().isoformat(timespec="seconds")
    with _connect() as conn:
        conn.execute(
            "INSERT INTO entries (date, customer, hours, description, created_at) VALUES (?, ?, ?, ?, ?)",
            (date_str, customer, float(hours), description, created_at),
        )


def get_entries(date_from=None, date_to=None, customer=None):
    query = "SELECT * FROM entries WHERE 1=1"
    params = []
    if date_from:
        query += " AND date >= ?"
        params.append(date_from)
    if date_to:
        query += " AND date <= ?"
        params.append(date_to)
    if customer:
        query += " AND customer = ?"
        params.append(customer)
    query += " ORDER BY date DESC, id DESC"
    with _connect() as conn:
        return [dict(row) for row in conn.execute(query, params).fetchall()]


def get_customers():
    with _connect() as conn:
        rows = conn.execute(
            "SELECT DISTINCT customer FROM entries ORDER BY customer ASC"
        ).fetchall()
        return [row["customer"] for row in rows]


def delete_entry(entry_id):
    with _connect() as conn:
        conn.execute("DELETE FROM entries WHERE id = ?", (entry_id,))


def get_managed_customers():
    with _connect() as conn:
        rows = conn.execute(
            "SELECT name FROM customers ORDER BY name ASC"
        ).fetchall()
        return [row["name"] for row in rows]


def add_customer(name):
    created_at = datetime.now().isoformat(timespec="seconds")
    with _connect() as conn:
        conn.execute(
            "INSERT OR IGNORE INTO customers (name, created_at) VALUES (?, ?)",
            (name, created_at),
        )


def remove_customer(name):
    with _connect() as conn:
        conn.execute("DELETE FROM customers WHERE name = ?", (name,))
