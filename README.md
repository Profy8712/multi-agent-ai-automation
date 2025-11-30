# 🚀 Multi-Agent AI Automation  
### Automated LinkedIn Post Generation using Google Gemini + Google Sheets + FastAPI

This project implements a production-style **multi-agent AI workflow** where two AI personas collaborate to create and refine high-quality LinkedIn posts.  
The system also stores results in Google Sheets and exposes a REST API for external automations (n8n, Make, Zapier, frontend apps).

---

# ⭐ Overview

This workflow consists of two independent agents:

### ✍️ Agent A — Writer  
Creates a concise, concrete, buzzword-free LinkedIn draft based on a topic.

### 📝 Agent B — Editor  
Acts as a strict professional editor:
- critiques the draft  
- rewrites it into a sharper, punchier version  
- responds in structured JSON  

### 📊 Google Sheets Logging  
Each run automatically stores:
- timestamp  
- topic  
- writer draft  
- editor final version  
- token usage  
- estimated API cost  

### 🔌 REST API Endpoint  
FastAPI endpoint:

```
POST /generate-post
```

Allows triggering the workflow from:
- n8n  
- Make  
- Postman  
- Websites  
- Any external system

---

# 📂 Project Structure

```
multi_agent_gemini/
│
├── agents/
│   ├── writer_agent.py         # Agent A: draft generation
│   ├── editor_agent.py         # Agent B: critique + rewrite
│
├── utils/
│   ├── gemini_client.py        # Gemini API wrapper with safe fallbacks
│   ├── google_sheets.py        # Google Sheets logging
│
├── main.py                     # CLI version of the workflow
├── api.py                      # REST API (FastAPI)
├── requirements.txt
├── .env.example
└── README.md
```

---

# 🔧 Installation

### 1. Clone the repository

```bash
git clone https://github.com/Profy8712/multi-agent-ai-automation.git
cd multi-agent-ai-automation
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate    # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

# 🔑 Environment Variables

Create a `.env` file:

```
GEMINI_API_KEY=YOUR_GEMINI_KEY
GEMINI_MODEL_NAME=models/gemini-2.5-flash
TOKEN_PRICE=0.000002

GOOGLE_SHEETS_CREDENTIALS=credentials.json
GOOGLE_SHEETS_ID=YOUR_SPREADSHEET_ID
```

You can copy `.env.example` and fill in your values.

---

# ▶️ Running the Workflow (CLI Version)

```bash
python main.py
```

You will get:

- Writer draft  
- Editor critique  
- Final post  
- Token usage  
- Estimated cost  
- Google Sheets confirmation  

---

# 🌐 Running the REST API

Start the API server:

```bash
uvicorn api:app --reload
```

Open interactive docs:

👉 **http://127.0.0.1:8000/docs**

Send a POST request:

```json
{
  "topic": "The future of AI agents in business"
}
```

The response includes:

- draft  
- critique  
- final post  
- total tokens  
- cost  

---

# 📊 Google Sheets Setup

1. Create a Google Sheet  
2. Add header row:

```
Timestamp | Topic | Draft | Final Post | Total Tokens | Cost
```

3. In Google Cloud Console:
   - enable Google Sheets API  
   - enable Google Drive API  
   - create a Service Account  
   - download `credentials.json`  

4. Share the Google Sheet with:
```
your-service-account@project.iam.gserviceaccount.com
```

---

# 🔄 n8n Integration (Optional)

1. Create Webhook node  
2. Add HTTP node that calls:

```
POST http://your-server:8000/generate-post
```

3. Pass `topic` from webhook payload  
4. Use the API response anywhere in your automation

---

# 🛠️ Technologies Used

- Python  
- FastAPI  
- Google Gemini API  
- Google Sheets API (gspread)  
- pydantic  
- uvicorn  
- python-dotenv  

---

# 🧩 Future Enhancements

- Agent C: Auto-publishing to LinkedIn  
- API Key authentication for REST API  
- Dockerfile + containerization  
- GitHub Actions CI/CD  
- n8n/Make templates  
- Health-check endpoint  
- Error monitoring dashboard  

---

# 📄 License  
MIT — free for personal and commercial use.

---

# 👤 Author  
**Profy8712**  
GitHub: https://github.com/Profy8712
