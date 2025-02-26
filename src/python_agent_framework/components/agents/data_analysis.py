import json
import sqlite3
from crewai import Agent
from components.connections.database import fetch_invoice, DB_PATH

class DataAnalysisAgent:
    def __init__(self):
        self.agent = Agent(
            role="Data Analyst",
            goal="Validate invoice details, detect potential fraud, and generate financial insights.",
            backstory=(
                "This agent specializes in analyzing invoice data. It ensures invoices are correctly formatted, "
                "validates tax calculations, and detects potential fraud such as duplicate invoices or unusual tax rates. "
                "Additionally, it identifies spending trends to help businesses optimize their expenses."
            )
        )

    def validate_invoice(self, invoice_data):
        """Checks for missing fields and ensures tax & total calculations are correct."""
        errors = []
        if not invoice_data.get("Invoice_ID"):
            errors.append("Missing Invoice ID")
        if not invoice_data.get("Vendor"):
            errors.append("Missing Vendor Name")
        if invoice_data.get("Total_Amount") is None:
            errors.append("Missing Total Amount")
        if invoice_data.get("Tax") is None:
            errors.append("Missing Tax Amount")
        if not invoice_data.get("Due_Date"):
            errors.append("Missing Due Date")

        # Validate total amount calculation
        calculated_total = sum(item["Quantity"] * item["Price"] for item in invoice_data.get("Line_Items", []))
        if abs(calculated_total - invoice_data.get("Total_Amount", 0)) > 1.0:
            errors.append(f"Total Amount Mismatch: Expected {calculated_total}, but got {invoice_data['Total_Amount']}")

        return {
            "valid": len(errors) == 0,
            "errors": errors
        }

    def detect_fraud(self, invoice_data, past_invoices):
        """Detects duplicate invoices and unusual tax rates."""
        warnings = []

        # Check for duplicate invoices in the database
        for past_invoice in past_invoices:
            if (invoice_data["Vendor"] == past_invoice["Vendor"] and
                invoice_data["Total_Amount"] == past_invoice["Total_Amount"] and
                invoice_data["Due_Date"] == past_invoice["Due_Date"]):
                warnings.append("⚠️ Potential Duplicate Invoice Detected.")

        # Check for unusually high tax rates
        if invoice_data["Tax"] > 0.3 * invoice_data["Total_Amount"]:  # More than 30% tax
            warnings.append("⚠️ Unusually High Tax Rate Detected.")

        return {
            "fraud_detected": len(warnings) > 0,
            "warnings": warnings
        }

    def get_past_invoices(self, exclude_invoice_id):
        """Fetches all past invoices from the database except the one currently being analyzed."""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM invoices WHERE invoice_id != ?", (exclude_invoice_id,))
        past_invoices = cursor.fetchall()
        
        conn.close()

        # Convert past invoices into list of dictionaries
        return [
            {
                "Invoice_ID": inv[0],
                "Vendor": inv[1],
                "Total_Amount": inv[2],
                "Tax": inv[3],
                "Due_Date": inv[4],
                "Line_Items": json.loads(inv[5])
            }
            for inv in past_invoices
        ]

    def analyze_invoice(self, invoice_id):
        """Fetches invoice from database and runs validation + fraud detection."""
        invoice_data = fetch_invoice(invoice_id)
        if not invoice_data:
            return {"error": "Invoice not found in database."}

        # Fetch all past invoices for comparison
        past_invoices = self.get_past_invoices(invoice_id)

        validation_results = self.validate_invoice(invoice_data)
        fraud_results = self.detect_fraud(invoice_data, past_invoices)

        return {
            "Invoice_ID": invoice_id,
            "Validation": validation_results,
            "Fraud Detection": fraud_results
        }
