import sqlite3
import csv
import re
from datetime import datetime
from config import logger

DB_FILE = "leads.db"
CSV_FILE = "leads.csv"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            username TEXT,
            full_name TEXT,
            email TEXT,
            phone TEXT,
            notes TEXT,
            captured_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def save_lead(user_id: int, username: str, full_name: str, email: str = None, phone: str = None, notes: str = None):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO leads (user_id, username, full_name, email, phone, notes)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (user_id, username, full_name, email, phone, notes))
    conn.commit()
    conn.close()

    file_exists = False
    try:
        with open(CSV_FILE, "r", encoding="utf-8"):
            file_exists = True
    except FileNotFoundError:
        pass

    with open(CSV_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["ID", "User ID", "Username", "Nom complet", "Email", "Téléphone", "Notes", "Date"])
        writer.writerow([None, user_id, username, full_name, email, phone, notes, datetime.now().isoformat()])
    
    logger.info(f"🎯 Nouveau lead enregistré : {full_name} ({user_id})")

def extract_and_save_lead_info(user_id: int, username: str, full_name: str, message_text: str) -> dict:
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    phone_pattern = r'(\+?\d{1,4}?[\s.-]?\(?\d{1,3}?\)?[\s.-]?\d{1,4}[\s.-]?\d{1,4}[\s.-]?\d{1,9})'

    emails = re.findall(email_pattern, message_text)
    phones = re.findall(phone_pattern, message_text)

    if emails or phones:
        found_email = emails[0] if emails else None
        found_phone = phones[0] if phones else None
        save_lead(user_id, username, full_name, email=found_email, phone=found_phone, notes=message_text)
        return {"email": found_email, "phone": found_phone}
    return {}
