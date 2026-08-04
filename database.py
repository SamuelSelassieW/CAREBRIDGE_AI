import sqlite3
from datetime import datetime

DB_NAME = "carebridge_records.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Maternal table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS maternal_visits (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        visit_date TEXT,
        risk_level TEXT,
        risk_score INTEGER,
        referred INTEGER,
        referral_message TEXT
    )
    """)

    # Nutrition table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS nutrition_visits (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        child_name TEXT,
        age_months INTEGER,
        muac REAL,
        malnutrition_level TEXT,
        visit_date TEXT,
        referred INTEGER
    )
    """)

    conn.commit()
    conn.close()


# ✅ Maternal Save
def save_patient(name, risk_level, risk_score, referred,
                 patient_data=None, referral_message=""):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO maternal_visits (
        name, visit_date, risk_level, risk_score, referred, referral_message
    )
    VALUES (?, ?, ?, ?, ?, ?)
    """, (
        name,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        risk_level,
        risk_score,
        int(referred),
        referral_message
    ))

    conn.commit()
    conn.close()


# ✅ Nutrition Save
def save_nutrition(child_name, age_months, muac,
                   malnutrition_level, referred):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO nutrition_visits (
        child_name, age_months, muac,
        malnutrition_level, visit_date, referred
    )
    VALUES (?, ?, ?, ?, ?, ?)
    """, (
        child_name,
        age_months,
        muac,
        malnutrition_level,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        int(referred)
    ))

    conn.commit()
    conn.close()