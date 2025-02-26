# Python Agent Framework for Invoice Processing

This project is a **multi-agent system** designed to automate invoice processing using AI.  
It extracts invoice details, validates them, detects fraud, notifies vendors/finance teams, and updates ERP systems.

---

## **🚀 Features**
✅ **Invoice Data Extraction** → Uses **Gemini AI** to extract invoice details from images.  
✅ **Validation & Fraud Detection** → Checks for **duplicate invoices, missing fields, tax mismatches,** etc.  
✅ **Automated Notifications** → Vendors & finance teams are alerted when necessary.  
✅ **ERP Integration (Simulated)** → Updates invoice status & triggers payments.  
✅ **Database Storage** → Uses **SQLite** to store invoices securely.  
✅ **Multi-Agent Orchestration** → Uses **CrewAI** to coordinate agent execution.  
✅ **Docker Support** → Containerized for easy deployment.  

---

## Prerequisites
### Install Docker or alternative

[Rancher Desktop](https://rancherdesktop.io/)

### API Keys
This project requires API Keys for the following services for which you will need to create accounts.

Create a .env file to store these keys
```plaintext
JUPYTER_TOKEN
OPENAI_API_KEY
LANGCHAIN_API_KEY
ANTHROPIC_API_KEY
HUGGINFACE_TOKEN
GOOGLE_API_KEY
```

### Starting the container
To start the container, run:

```sh
docker compose up
```

### Stoping the container
```sh
docker compose down
```

enter the container using the command: docker exec -it <container_id> /bin/sh

### To run the app
```sh
python src/python_agent_framework/main.py
```
### PATH to the testing images:
```sh
/code/src/python_agent_framework/data/image_2.jpg
``` 

## **📂 Project Structure**
```plaintext
python_agent_framework/
│── components/                      # Core framework components
│   │── agents/                       # AI Agents 
│   │   │── __init__.py                # Registers all agents
│   │   │── document_processor.py      # Extracts & structures invoice data
│   │   │── data_analysis.py           # Validates invoices, detects fraud
│   │   │── customer_interaction.py    # Notifies vendors & finance teams
│   │   │── task_execution.py          # Updates ERP, flags fraud, triggers payments
│   │── connections/                    # Database & API connections
│   │   │── __init__.py                 # Registers connections
│   │   │── database.py                 # SQLite database management
│── core/                              # Core framework component base classes
│   │── agent_flow.py                   # Governs agent behavior pattern (e.g., ReAct)
│   │── agent.py                        # Agent base class
│   │── connection.py                    # LLM connection configuration
│   │── memory.py                        # Basic memory implementation
│   │── tool_manager.py                  # Manages tool execution
│   │── tool.py                          # Tool base class
│── data/                              # Sample invoice images
│   │── image_1.jpg                     # Sample invoice image 1
│   │── image_2.jpg                     # Sample invoice image 2
|   |── image_3.jpg                     # Sample invoice image 3
│── llm/                               # LLM Helpers
│   │── chat_completion.py               # OpenAI / Gemini Chat model calls
│── utilities/                          # Helper scripts
│   │── pretty_print_conversation.py     # Prints structured conversation logs
│── main.py                            # Main entry point for the AI workflow
│── Dockerfile                         # Docker container configuration
│── requirements.txt                    # Python dependencies
│── .env                                # Environment variables (API Keys)
│── README.md                           # Documentation
