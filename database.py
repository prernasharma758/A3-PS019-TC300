import sqlite3
import pandas as pd

DB_FILE = "privacy_evidence.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS evidence (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_name TEXT,
            pii_type TEXT,
            leaked_value TEXT,
            risk_level TEXT,
            compliance_status TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def insert_evidence(file_name, pii_type, leaked_value, risk_level, compliance_status):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO evidence (file_name, pii_type, leaked_value, risk_level, compliance_status)
        VALUES (?, ?, ?, ?, ?)
    ''', (file_name, pii_type, leaked_value, risk_level, compliance_status))
    conn.commit()
    conn.close()

def get_all_evidence():
    conn = sqlite3.connect(DB_FILE)
    df = pd.read_sql_query('''
        SELECT file_name AS "File Name", 
               pii_type AS "PII Type", 
               leaked_value AS "Leaked Value (Masked)", 
               risk_level AS "Risk Level", 
               compliance_status AS "Compliance Status", 
               timestamp AS "Timestamp" 
        FROM evidence 
        ORDER BY id DESC
    ''', conn)
    conn.close()
    return df

def clear_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM evidence')
    conn.commit()
    conn.close()
