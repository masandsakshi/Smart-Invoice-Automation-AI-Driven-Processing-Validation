from components.agents.data_analysis import DataAnalysisAgent

# Sample valid invoice data
valid_invoice = {
    "Invoice_ID": "INV-123456",
    "Vendor": "ABC Supplies",
    "Total_Amount": 1050.75,
    "Tax": 50.75,
    "Due_Date": "2025-03-15",
    "Line_Items": [
        {"Item": "Laptop", "Quantity": 1, "Price": 1000.00},
        {"Item": "Mouse", "Quantity": 1, "Price": 50.75}
    ]
}

# Sample fraudulent invoice data (duplicate & high tax rate)
fraud_invoice = {
    "Invoice_ID": "INV-654321",
    "Vendor": "ABC Supplies",
    "Total_Amount": 200.00,
    "Tax": 90.00,  # 45% tax (too high)
    "Due_Date": "2025-03-20",
    "Line_Items": [
        {"Item": "Keyboard", "Quantity": 2, "Price": 100.00}
    ]
}

# Initialize Data Analysis Agent
data_analyst = DataAnalysisAgent()

# Run test cases
print("\n🚀 Running Data Analysis Agent Test...\n")

print("🔹 Case 1: Valid Invoice")
print(data_analyst.validate_invoice(valid_invoice))
print(data_analyst.detect_fraud(valid_invoice, []))

print("\n🔹 Case 2: Fraudulent Invoice")
print(data_analyst.validate_invoice(fraud_invoice))
print(data_analyst.detect_fraud(fraud_invoice, [valid_invoice]))  # Checking against past invoice
