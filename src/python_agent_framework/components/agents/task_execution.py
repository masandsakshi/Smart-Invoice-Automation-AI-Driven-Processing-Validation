import sqlite3
from crewai import Agent
from components.connections.database import fetch_invoice, DB_PATH

class TaskExecutionAgent:
    def __init__(self):
        self.agent = Agent(
            role="Task Execution Agent",
            goal="Update the ERP system, flag fraudulent invoices, and trigger payment processing.",
            backstory=(
                "This agent is responsible for executing final invoice-related tasks. "
                "It updates the ERP system with approved invoices, flags fraudulent ones, "
                "and ensures smooth financial operations."
            )
        )

    def update_invoice_status(self, invoice_id, status):
        """Updates the invoice status in the database."""
        conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        cursor = conn.cursor()

        cursor.execute("UPDATE invoices SET status = ? WHERE invoice_id = ?", (status, invoice_id))
        conn.commit()
        conn.close()

    def process_invoice(self, invoice_id, fraud_detected):
        """Handles final processing of the invoice."""
        invoice_data = fetch_invoice(invoice_id)
        if not invoice_data:
            print(f"⚠️ Error: Invoice {invoice_id} not found.")
            return

        if fraud_detected:
            print(f"🚨 Fraud detected! Flagging Invoice {invoice_id} as 'Flagged'.")
            self.update_invoice_status(invoice_id, "Flagged")
            return

        # Simulate ERP update
        print(f"✅ Updating ERP System for Invoice {invoice_id}...")
        self.update_invoice_status(invoice_id, "Approved")

        # Simulate payment trigger
        print(f"💰 Payment for Invoice {invoice_id} has been scheduled.")
