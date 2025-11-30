# 🚀 Multi-Agent AI Automation
### Automated LinkedIn Post Generation using Google Gemini + Google Sheets + FastAPI + Docker + n8n

This project provides a **production-grade multi-agent automation system** integrating:

- **Google Gemini AI** (Writer Agent + Editor Agent)  
- **Google Sheets logging**
- **FastAPI REST API**
- **Docker containerization**
- **GitHub Actions CI/CD**
- **n8n workflow automation (Webhook → AI → Sheets)**

All components together form an end‑to‑end automated content generation pipeline.

---

# ⭐ Features

## ✍️ Agent A — Writer  
Generates a LinkedIn-style draft based on a topic.  
Characteristics:
- No buzzwords
- No emojis / hashtags  
- Max 5 sentences  
- Natural, professional tone  
- Retry logic for empty Gemini responses  
- Robust error handling  

---

## 📝 Agent B — Editor  
A strict editor persona that:
- Critiques the draft (max 3 sentences)
- Rewrites it in a stronger, punchier tone
- ALWAYS returns **valid JSON**:
```json
{
  "critique": "...",
  "final_post": "..."
}
```

The system automatically:
- Cleans malformed JSON  
- Removes backticks, markdown fences  
- Ensures structured output  

---

## 📊 Google Sheets Logging  
Every processed request is saved with:

- Timestamp  
- Topic  
- Writer Draft  
- Editor Final Post  
- Total Tokens  
- Estimated Cost  

Google Sheets is accessed via a **Google Service Account**.

---

## 🌐 REST API (FastAPI)

Main endpoint:

### `POST /generate-post`

Input:
```json
{ "topic": "Your topic here" }
```

Output:
```json
{
  "draft": "...",
  "critique": "...",
  "final_post": "...",
  "tokens": 123,
  "cost": 0.000246
}
```

Interactive API docs:  
👉 http://localhost:8000/docs

---

## 🐳 Docker Support

Build and run the service in background:

```bash
docker compose up -d --build
```

Stop:
```bash
docker compose down
```

API will be available at:
👉 http://localhost:8000

---

## 🔄 n8n Workflow Automation

A complete workflow is included:

**File:**  
```
/n8n_multi_agent_workflow.json
```

### Workflow steps:
1. Webhook trigger  
2. Agent A — Writer call  
3. Agent B — Editor call  
4. Error-handling path (JSON check, retries)  
5. Google Sheets append  
6. Respond with final JSON  

### Import instructions:

1. Open **n8n**
2. Go to **Workflows → Import**
3. Upload:  
   ```
   n8n_multi_agent_workflow.json
   ```
4. Configure credentials:
   - Gemini API Key
   - Google Sheets Service Account
5. Activate workflow

### Webhook usage:
You will get a link like:

```
POST https://n8n.your-domain.com/webhook/ai-post-generator
```

Body:
```json
{ "topic": "The future of AI Agents in Business" }
```

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
├── n8n_multi_agent_workflow.json
├── requirements.txt
├── .env.example
└── README.md
```

---

# 🔧 Installation

Clone repo:

```bash
git clone https://github.com/Profy8712/multi-agent-ai-automation.git
cd multi-agent-ai-automation
```

Create env:

```bash
python -m venv venv
source venv/bin/activate      # macOS / Linux
venv\Scripts\activate       # Windows
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# 🔑 Environment Variables

Create a `.env`:

```
GEMINI_API_KEY=YOUR_KEY
GEMINI_MODEL_NAME=models/gemini-2.5-flash
TOKEN_PRICE=0.000002

GOOGLE_SHEETS_CREDENTIALS=credentials.json
GOOGLE_SHEETS_ID=YOUR_SPREADSHEET_ID
```

---

# ▶️ Run from CLI

```bash
python main.py
```

---

# 🌐 Run API server

```bash
uvicorn api:app --reload
```

Docs: http://127.0.0.1:8000/docs

---

# ⚙️ CI/CD – GitHub Actions

The project includes a production-ready pipeline:

### ✔️ On push to `main`:
- Install Python  
- Lint & syntax check  
- Build Docker image  
- Push image to Docker Hub  
- Validate workflow  

Config file:  
```
.github/workflows/ci-cd.yml
```

### Required GitHub secrets:

| Secret | Purpose |
|--------|---------|
| `DOCKERHUB_USERNAME` | Docker Hub login |
| `DOCKERHUB_TOKEN` | Access token |
| `GOOGLE_SHEETS_ID` | Spreadsheet |
| `GEMINI_API_KEY` | Gemini auth |

---

# 🧩 Error Handling

### Gemini client handles:
- Empty responses  
- Blocked responses  
- Missing parts  
- JSON parse errors  
- Auto‑retry logic  

### API layer handles:
- Missing topic field  
- Upstream AI errors  
- Sheets write failures  
- HTTP 500 wrapping  

### n8n workflow handles:
- JSON validation  
- Retry on Gemini call  
- Fallback response  
- Structured logging  

---

# 🛠️ Technologies
- Python 3.11  
- FastAPI  
- Google Gemini API  
- gspread  
- Uvicorn  
- Docker + Docker Compose  
- GitHub Actions  
- n8n workflow engine  

---

# 👤 Author
**Profy8712**  
https://github.com/Profy8712
