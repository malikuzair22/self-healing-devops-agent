import sqlite3
import json
from datetime import datetime

def init_db():
    conn = sqlite3.connect("incidents.db")
    cursor = conn.cursor()

    cursor.execute("""
          CREATE TABLE IF NOT EXISTS incidents(
            incident_id TEXT PRIMARY KEY,
            source TEXT,
            diagnosis TEXT,
            confidence REAL,
            action_taken TEXT,
            status TEXT,
            timestamp TEXT
          )
    """)
    conn.commit()
    conn.close()

def save_incidents(incident: dict):
    conn = sqlite3.connect('incidents.db')
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO incidents VALUES(?,?,?,?,?,?,?)
    """, (incident['incident_id'], incident['source'], incident['diagnosis'], 
           incident['confidence'], incident['action_taken'], 
            incident['status'],
            datetime.now().isoformat()))
    conn.commit()
    conn.close()


def get_incidents():
    conn = sqlite3.connect("incidents.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM incidents")
    rows = cursor.fetchall()
    conn.close()
    return rows






