import smtplib
from email.mime.text import MIMEText
from crewai import Agent
from components.connections.database import fetch_invoice

class CustomerInteractionAgent:
    def __init__(self):
        self.agent = Agent(
            role="Customer Interaction Agent",
            goal="Communicate invoice status to vendors and finance teams.",
            backstory=(
                "This agent ensures smooth communication between the company and vendors. "
                "It automatically notifies vendors about their invoice status and alerts the finance team "
                "if any fraud is detected, ensuring transparency and efficiency in invoice processing."
            )
        )

    def send_email(self, recipient, subject, body):
        """Sends an email notification (MVP: Replace with actual SMTP credentials)."""
        print(f"\n📧 Sending Email to {recipient}...")
        print(f"📌 Subject: {subject}")
        print(f"📝 Body: {body}\n")

    def notify_vendor(self, invoice_id):
        """Notifies the vendor about invoice status."""
        invoice_data = fetch_invoice(invoice_id)
        if not invoice_data:
            print("⚠️ Error: Invoice not found.")
            return

        vendor_email = f"{invoice_data['Vendor'].replace(' ', '').lower()}@example.com"  # Placeholder email

        subject = "Your Invoice is Being Processed"
        body = (
            f"Hello {invoice_data['Vendor']},\n\n"
            f"Your invoice (ID: {invoice_data['Invoice_ID']}) of ${invoice_data['Total_Amount']} "
            f"has been successfully processed. Payment will be made by the due date: {invoice_data['Due_Date']}.\n\n"
            "Thank you for your business.\nBest regards,\nFinance Team"
        )

        self.send_email(vendor_email, subject, body)

    def notify_finance_team(self, invoice_id, fraud_warnings):
        """Notifies the finance team if fraud is detected."""
        finance_email = "finance-team@example.com"  # Placeholder email

        subject = "⚠️ Fraud Alert: Invoice Needs Review"
        body = (
            f"Attention Finance Team,\n\n"
            f"The following invoice has been flagged for potential fraud:\n"
            f"Invoice ID: {invoice_id}\n"
            f"Issues Detected:\n"
            + "\n".join([f"❌ {warning}" for warning in fraud_warnings]) +
            "\n\nPlease review this invoice manually.\nBest regards,\nAutomated Invoice System"
        )

        self.send_email(finance_email, subject, body)

    def handle_invoice_communication(self, invoice_id, validation_results, fraud_results):
        """Decides whether to notify the vendor or escalate to finance team."""
        if not validation_results["valid"]:
            print(f"❌ Invoice {invoice_id} has errors and will not be processed.")
            return

        if fraud_results["fraud_detected"]:
            print(f"🚨 Fraud detected for Invoice {invoice_id}. Escalating to finance team...")
            self.notify_finance_team(invoice_id, fraud_results["warnings"])
        else:
            print(f"✅ Invoice {invoice_id} is valid. Notifying vendor...")
            self.notify_vendor(invoice_id)
