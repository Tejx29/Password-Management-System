import sqlite3

def init_db():
    conn = sqlite3.connect("data/vault.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS vault (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            site TEXT,
            username TEXT,
            nonce BLOB,
            password BLOB
        )
    """)
    conn.commit()
    conn.close()

def add_entry(site, username, nonce, password):
    conn = sqlite3.connect("data/vault.db")
    c = conn.cursor()
    c.execute("INSERT INTO vault (site, username, nonce, password) VALUES (?, ?, ?, ?)",
              (site, username, nonce, password))
    conn.commit()
    conn.close()

def get_entry(site):
    conn = sqlite3.connect("data/vault.db")
    c = conn.cursor()
    c.execute("SELECT username, nonce, password FROM vault WHERE site=?", (site,))
    row = c.fetchone()
    conn.close()
    return row
