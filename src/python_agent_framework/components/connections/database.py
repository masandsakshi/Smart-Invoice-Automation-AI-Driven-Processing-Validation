import sqlite3
import json
import os

# Define database path
DB_PATH = "src/python_agent_framework/invoices.db"




def init_db():
    """Initialize the SQLite database for storing invoices."""
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)  # Allows multiple agents to access DB
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS invoices (
            invoice_id TEXT PRIMARY KEY,
            vendor TEXT,
            total_amount REAL,
            tax REAL,
            due_date TEXT,
            line_items TEXT,  -- JSON String
            status TEXT  -- "Pending", "Flagged", "Approved"
        )
    """)
    conn.commit()
    conn.close()

def save_invoice(invoice_data):
    """Save extracted invoice data into the database, avoiding duplicates."""
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    cursor = conn.cursor()

    # Check if invoice already exists
    cursor.execute("SELECT invoice_id FROM invoices WHERE invoice_id = ?", (invoice_data["Invoice_ID"],))
    existing_invoice = cursor.fetchone()

    if existing_invoice:
        print(f"⚠️ Warning: Invoice {invoice_data['Invoice_ID']} already exists in the database. Skipping insertion.")
        conn.close()
        return  # Exit without inserting duplicate invoice

    cursor.execute("""
        INSERT INTO invoices (invoice_id, vendor, total_amount, tax, due_date, line_items, status)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        invoice_data["Invoice_ID"],
        invoice_data["Vendor"],
        invoice_data["Total_Amount"],
        invoice_data["Tax"],
        invoice_data["Due_Date"],
        json.dumps(invoice_data["Line_Items"]),  # Convert list to JSON string
        "Pending"
    ))

    conn.commit()
    conn.close()

def fetch_invoice(invoice_id):
    """Retrieve an invoice from the database using invoice_id."""
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM invoices WHERE invoice_id = ?", (invoice_id,))
    invoice = cursor.fetchone()
    
    conn.close()
    
    if invoice:
        return {
            "Invoice_ID": invoice[0],
            "Vendor": invoice[1],
            "Total_Amount": invoice[2],
            "Tax": invoice[3],
            "Due_Date": invoice[4],
            "Line_Items": json.loads(invoice[5]),
            "Status": invoice[6]
        }
    else:
        return None

