import sqlite3
from pathlib import Path


# Database location
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "finance.db"


# ============================================================
# CREATE DATABASE
# ============================================================

def create_database():

    connection = sqlite3.connect(DB_PATH)

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            Date TEXT NOT NULL,
            Category TEXT NOT NULL,
            Amount REAL NOT NULL,
            Description TEXT
        )
    """)

    connection.commit()
    connection.close()


# ============================================================
# ADD EXPENSE
# ============================================================

def add_expense(expense_date, category, amount, description):

    connection = sqlite3.connect(DB_PATH)

    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO expenses
        (Date, Category, Amount, Description)
        VALUES (?, ?, ?, ?)
    """, (
        str(expense_date),
        category,
        amount,
        description
    ))

    connection.commit()
    connection.close()


# ============================================================
# GET EXPENSES
# ============================================================

def get_expenses():

    connection = sqlite3.connect(DB_PATH)

    cursor = connection.cursor()

    cursor.execute("""
        SELECT Date, Category, Amount, Description
        FROM expenses
        ORDER BY Date
    """)

    rows = cursor.fetchall()

    connection.close()

    expenses = []

    for row in rows:

        expenses.append({
            "Date": row[0],
            "Category": row[1],
            "Amount": row[2],
            "Description": row[3]
        })

    return expenses


# ============================================================
# INITIALIZE DATABASE
# ============================================================

create_database()