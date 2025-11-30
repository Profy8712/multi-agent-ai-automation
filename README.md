# 🚀 Multi-Agent AI Automation  
### Automated LinkedIn Post Generation using Google Gemini + Google Sheets + FastAPI + Docker

This project implements a production-ready **multi-agent AI workflow** where:
- **Agent A (Writer)** generates a LinkedIn draft  
- **Agent B (Editor)** critiques and improves the draft in strict JSON  
- Everything is logged into **Google Sheets**  
- A **REST API** exposes the workflow  
- The entire service runs inside **Docker**

---

# ⭐ Overview

### ✍️ Agent A — Writer  
Creates concise, concrete, buzzword-free LinkedIn-style drafts.  
Includes retry logic when Gemini returns empty responses.

### 📝 Agent B — Editor  
Strict editorial persona:  
- provides critique  
- rewrites content  
- always returns JSON  
- automatically cleans malformed model outputs

### 📊 Google Sheets Logging  
Each run saves:
- Timestamp  
- Topic  
- Writer draft  
- Final edited version  
- Token usage  
- Estimated cost  

### 🌐 REST API (FastAPI)
Main endpoint:

```
POST /generate-post
```

Input:
```json
{ "topic": "Your topic here" }
```

Output:
- draft  
- critique  
- final_post  
- tokens  
- cost  

Swagger docs:  
👉 http://localhost:8000/docs

---

# 📂 Project Structure

```
multi_agent_gemini/
│
├── agents/
│   ├── writer_agent.py
│   ├── editor_agent.py
│
├── utils/
│   ├── gemini_client.py
│   ├── google_sheets.py
│
├── api.py
├── main.py
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
├── requirements.txt
├── .env.example
└── README.md
```

---

# 🔧 Installation

Clone the project:

```bash
git clone https://github.com/Profy8712/multi-agent-ai-automation.git
cd multi-agent-ai-automation
```

Create virtual environment:

```bash
python -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate    # Windows
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# 🔑 Environment Variables

Create a `.env` file:

```
GEMINI_API_KEY=YOUR_KEY
GEMINI_MODEL_NAME=models/gemini-2.5-flash
TOKEN_PRICE=0.000002

GOOGLE_SHEETS_CREDENTIALS=credentials.json
GOOGLE_SHEETS_ID=YOUR_SHEET_ID
```

Copy `.env.example` as baseline if needed.

---

# ▶️ Running via Python

```bash
python main.py
```

---

# 🌐 Running REST API

Start server:

```bash
uvicorn api:app --reload
```

Swagger docs:

👉 http://127.0.0.1:8000/docs

---

# 🐳 Docker Support

### Build + run in background:

```bash
docker compose up -d --build
```

### Stop:

```bash
docker compose down
```

API available at:

👉 http://localhost:8000

---

# 📊 Google Sheets Setup

1. Create Google Sheet  
2. Header row:

```
Timestamp | Topic | Draft | Final Post | Total Tokens | Cost
```

3. Enable Sheets + Drive API  
4. Create Service Account  
5. Download `credentials.json`  
6. Share Sheet with service account email

---

# 🧩 Technologies Used
- FastAPI  
- Google Gemini API  
- gspread  
- Uvicorn  
- Docker  
- Python 3.11  

---

# 🛠️ Future Enhancements
- Agent C (auto publishing)  
- Authentication for REST API  
- GitHub Actions (CI/CD)  
- Multi-stage production Dockerfile  
- Monitoring & logging dashboard  

---

# 👤 Author  
**Profy8712**  
https://github.com/Profy8712
