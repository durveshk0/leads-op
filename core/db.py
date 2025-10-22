import sqlite3, os
from datetime import datetime
import re

DB_PATH = "leads.db"
os.makedirs(os.path.dirname(DB_PATH) or ".", exist_ok=True)

def conn_factory():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def init_db():
    conn = conn_factory()
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS leads (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT UNIQUE,
        message TEXT,
        score INTEGER,
        classification TEXT,
        last_contacted TEXT,
        created_at TEXT
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        lead_id INTEGER,
        event TEXT,
        details TEXT,
        created_at TEXT
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS retrain_queue (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        message TEXT,
        score INTEGER,
        classification TEXT,
        extra_credit INTEGER DEFAULT 0,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
    """)
    

    conn.commit()
    conn.close()

def insert_lead(name, email, message, score, classification):
    now = datetime.utcnow().isoformat()
    conn = conn_factory(); c = conn.cursor()
    c.execute("""INSERT OR REPLACE INTO leads 
        (name,email,message,score,classification,created_at,last_contacted)
        VALUES (?,?,?,?,?,?,?)""",
        (name, email, message, score, classification, now, now))
    conn.commit(); conn.close()

def update_lead_contact(email):
    conn = conn_factory(); c = conn.cursor()
    c.execute("UPDATE leads SET last_contacted=? WHERE email=?",
              (datetime.utcnow().isoformat(), email))
    conn.commit(); conn.close()


def get_all_leads():
    conn = conn_factory(); c = conn.cursor()
    c.execute("SELECT * FROM leads ORDER BY id DESC")
    rows = c.fetchall(); conn.close()
    return rows

def log_event(lead_id, event, details=""):
    conn = conn_factory(); c = conn.cursor()
    c.execute("INSERT INTO logs (lead_id,event,details,created_at) VALUES (?,?,?,?)",
              (lead_id, event, details, datetime.utcnow().isoformat()))
    conn.commit(); conn.close()

def add_to_retrain_queue(name, email, message, score, classification):
    extra_credit = 0
    # Add extra credit for business/company emails
    if re.search(r'\.(in|com|co|tech)$', email.lower()):
        extra_credit = 10
    conn = conn_factory()
    c = conn.cursor()
    c.execute("""
        INSERT INTO retrain_queue (name, email, message, score, classification, extra_credit)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (name, email, message, score, classification, extra_credit))
    conn.commit(); conn.close() 