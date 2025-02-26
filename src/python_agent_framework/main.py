from components.agents.document_processor import DocumentProcessorAgent
from components.agents.data_analysis import DataAnalysisAgent
from components.agents.customer_interaction import CustomerInteractionAgent
from components.agents.task_execution import TaskExecutionAgent
from components.connections.database import fetch_invoice, init_db
import os

def main():
    print("\n🤖 Hello! I'm your Invoice Processing Assistant.")

    # Initialize database
    init_db()

    doc_processor = DocumentProcessorAgent()
    data_analyst = DataAnalysisAgent()
    customer_interaction = CustomerInteractionAgent()
    task_executor = TaskExecutionAgent()

    while True:
        invoice_path = input("\n📂 Please enter the path to your invoice image (or type 'exit' to quit): ").strip()

        if invoice_path.lower() == "exit":
            print("\n👋 Goodbye! Have a great day!\n")
            break

        if not os.path.exists(invoice_path):
            print("\n⚠️ Error: The file does not exist. Please try again.")
            continue

        # Step 1: Process the invoice and store in the database
        print("\n🚀 Processing your invoice...")
        extracted_data = doc_processor.process_invoice(invoice_path)

        if "error" in extracted_data:
            print(f"⚠️ Invoice processing failed. Error: {extracted_data['error']}")
            continue

        print("\n📄 Extracted Invoice Data (Stored in Database):")
        print(extracted_data)

        # Step 2: Analyze the invoice
        invoice_id = extracted_data["Invoice_ID"]
        print("\n📊 Running Data Analysis...")
        analysis_results = data_analyst.analyze_invoice(invoice_id)

        # Display validation and fraud detection results
        print("\n✅ Validation Results:")
        if analysis_results["Validation"]["valid"]:
            print("✔️ Invoice is valid.")
        else:
            print("❌ Invoice has errors:", analysis_results["Validation"]["errors"])

        print("\n🚨 Fraud Detection Results:")
        if analysis_results["Fraud Detection"]["fraud_detected"]:
            print("⚠️ WARNING: Potential fraud detected!")
            for warning in analysis_results["Fraud Detection"]["warnings"]:
                print(f"❌ {warning}")
        else:
            print("✔️ No fraud detected.")

        # Step 3: Handle notifications
        print("\n📢 Sending notifications...")
        customer_interaction.handle_invoice_communication(
            invoice_id,
            analysis_results["Validation"],
            analysis_results["Fraud Detection"]
        )

        # Step 4: Execute Final Invoice Actions
        print("\n🛠️ Executing Task Actions...")
        task_executor.process_invoice(invoice_id, analysis_results["Fraud Detection"]["fraud_detected"])

        # Fetch and display stored invoice details
        stored_invoice = fetch_invoice(invoice_id)
        print("\n🗄️ Invoice Retrieved from Database:")
        print(stored_invoice)

if __name__ == "__main__":
    main()
