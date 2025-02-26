from components.agents.document_processor import DocumentProcessorAgent
import json

# Initialize the Document Processor Agent
doc_processor = DocumentProcessorAgent()

# Provide the actual path to an invoice image
invoice_path = "/code/src/python_agent_framework/data/image_2.jpg"  # <-- Replace with actual invoice image path


# Run the document processor agent
print("Processing Invoice...")
invoice_data = doc_processor.process_invoice(invoice_path)
