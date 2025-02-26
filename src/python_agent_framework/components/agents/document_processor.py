import google.generativeai as genai
import os
from dotenv import load_dotenv
import base64
import json
from crewai import Agent
from components.connections.database import save_invoice, init_db

# Load API Key
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Configure Gemini API
genai.configure(api_key=GOOGLE_API_KEY)

class DocumentProcessorAgent:
    def __init__(self):
        self.agent = Agent(
            role="Document Processor",
            goal=(
                "Extract structured information from invoice images "
                "using state-of-the-art AI models and convert it into a machine-readable JSON format."
            ),
            backstory=(
                "This agent specializes in intelligent document processing, utilizing advanced AI-driven OCR "
                "and Natural Language Processing (NLP) techniques. It ensures accurate extraction of "
                "key financial information from invoices, including vendor details, invoice ID, line items, "
                "total amounts, taxes, and due dates. By leveraging cutting-edge AI, this agent minimizes "
                "human errors, detects missing fields, and prepares structured data for further financial processing. "
                "This extracted data will be crucial for downstream tasks such as validation, fraud detection, "
                "and enterprise integration into ERP systems."
            )
        )

        # Initialize database on startup
        init_db()

    def encode_image(self, image_path):
        """Convert image to base64 format for API processing."""
        try:
            with open(image_path, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode("utf-8")
        except Exception as e:
            return {"error": f"Failed to encode image: {str(e)}"}

    def extract_invoice_data(self, image_path):
        """Extract invoice data using Gemini 2.0 Flash API and store it in the database."""
        image_base64 = self.encode_image(image_path)
        if isinstance(image_base64, dict) and "error" in image_base64:
            return image_base64  # Return error if encoding failed

        try:
            # Initialize the Gemini model
            model = genai.GenerativeModel("gemini-2.0-flash")

            # Call Gemini API with image data
            response = model.generate_content(
                contents=[
                    {
                        "role": "user",
                        "parts": [
                            {"text": (
                                "Extract the invoice details from this image and return ONLY a valid Python dictionary.\n"
                                "Ensure the response **does NOT include any extra text, labels, or comments**.\n"
                                "Output should be **only the dictionary**, nothing else.\n"
                                "Example format:\n"
                                "{\n"
                                '  "Invoice_ID": "string",\n'
                                '  "Vendor": "string",\n'
                                '  "Total_Amount": float,\n'
                                '  "Tax": float,\n'
                                '  "Due_Date": "YYYY-MM-DD",\n'
                                '  "Line_Items": [\n'
                                '    {"Item": "string", "Quantity": int, "Price": float}\n'
                                '  ]\n'
                                "}"
                            )},
                            {"inline_data": {"mime_type": "image/jpeg", "data": image_base64}}
                        ]
                    }
                ]
            )

            # Debugging: Print raw response before processing
            extracted_text = response.text
            # print("\n🔍 RAW RESPONSE FROM GEMINI API:")
            # print(extracted_text)

            # FIX: Remove unwanted ```python and ``` from the response
            cleaned_text = extracted_text.strip("```python").strip("```").strip()

            # Convert cleaned text to dictionary
            invoice_data = json.loads(cleaned_text)

            # Store extracted invoice data in the database
            save_invoice(invoice_data)  

            return invoice_data  # Return structured invoice data

        except json.JSONDecodeError:
            return {"error": "Failed to parse API response as JSON. Response format may be incorrect."}
        except Exception as e:
            return {"error": f"Failed to extract invoice data: {str(e)}"}

    def process_invoice(self, image_path):
        """Main function to process invoice and return JSON."""
        return self.extract_invoice_data(image_path)
