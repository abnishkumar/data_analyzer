# 📄 AutoGen Agentic AI: Document Analyzer & Code Explanation App

This project uses **AutoGen**, an agentic AI framework by Microsoft, to build a smart document analyzer. It allows users to upload a document, ask questions, and see how Python code is generated and executed to analyze the data — along with a step-by-step explanation of the process.

---

## 🚀 Features

- Upload structured documents (like CSV).
- Ask natural language questions about the data.
- AutoGen agents:
  - Understand your question.
  - Write & run Python code to analyze the data.
  - Explain the code step-by-step.
- User-friendly interface built with **Streamlit**.
- Safe code execution using **Docker**.

---

## ⚙️ Setup Instructions

### 1. Clone the Project

```bash
git clone git@github.com:abnishkumar/data_analyzer.git
cd <your-project-folder>
```

### 2. Create a Virtual Environment

``` python -m venv .venv
# Activate environment
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate

```

### 3. Install Dependencies

pip install -r requirements.txt

### 4. Create .env Configuration File
- In the root directory, create a .env file and add:
```
    TIMEOUT_DOCKER=120
    WORK_DIR_DOCKER=temp
    MODEL_OPENAI=gpt-4o
    DEFAULT_MAX_TURNS=10
    DEFAULT_TERMINATION_PHRASE=STOP
    OPENAI_API_KEY=your-openai-api-key-here
```
### Run the Streamlit App

streamlit run streamlit_app.py

🧠 How It Works

- You upload a document (e.g., CSV).

- Ask a question like:

    "What’s the average sales in 2023?"

- The AI agents:

    Parse the file.

    Write Python code to get the answer.

    Run the code in Docker.

    Show the result and explain what the code did.

📚 Prerequisites

Make sure you have:

- Python (version >3.10) installed  (knowledge of OOPs recommended)

- AutoGen Framework

- Docker installed and running

- Streamlit installed via requirements.txt

TODO :

- Testing Strategy and Monitoring