# 🚀 Multi-Agent AI Automation
### Automated LinkedIn Post Generation using Google Gemini + Google Sheets + FastAPI + Docker + n8n

This repository contains a **production-grade multi-agent automation system** built to solve the **Technical Test Task: Multi-Agent AI Automation** and expanded into a full-scale, professional automation project.

The solution integrates:

- **Google Gemini AI** (Writer Agent + Editor Agent)
- **n8n workflow automation**
- **Google Sheets logging (via Service Account)**
- **FastAPI REST microservice**
- **Docker containerization**
- **GitHub Actions CI/CD pipeline**

It demonstrates real-world automation skills: AI orchestration, error handling, structured output validation, token & cost analytics, persistent logging, and deployment readiness.

---

# 🔥 Technical Test Solution Summary

## 🎯 Objective
Build a workflow where:
1. **Agent A (Writer)** generates a LinkedIn-style draft.  
2. **Agent B (Editor)** critiques & rewrites it in a punchier tone.  
3. System logs results + tokens + cost to Google Sheets.  
4. Workflow triggered via Webhook.

---

# 🧩 Workflow Summary (n8n)

### Steps:
1. Webhook Trigger  
2. Gemini Writer  
3. Gemini Editor  
4. JSON Validation  
5. Token & Cost Calculation  
6. Google Sheets Append  
7. JSON Response

Writer rules:
- No emojis / hashtags  
- No buzzwords  
- Max 5 sentences  

Editor rules:
- Strict editor persona  
- Critique (max 3 sentences)  
- Rewritten final post  
- Must output JSON:
```json
{"critique":"...","final_post":"..."}
```

---

# 📊 Token & Cost Calculation

Gemini provides:
- `promptTokenCount`
- `totalTokenCount`

Output tokens = `totalTokenCount - promptTokenCount`.

Pricing model included:
- Writer: $0.00035 input / $0.00070 output
- Editor: $0.00350 input / $0.01050 output

System automatically logs:
- Writer input/output
- Editor input/output
- Total tokens
- Estimated cost

---

# 🛡 Error Handling

### Includes:
- Empty Writer response → retry  
- Malformed JSON → repair  
- Hallucinated structure → cleanup  
- Too-long draft → trimming  
- Sheets write errors → safe handling  
- Missing topic → immediate error  

---

# 🚀 Extended Project Features

## ✍️ Agent A – Writer
- Short, clear LinkedIn drafts  
- Business tone  
- Retry logic  
- Safe defaults  

## 📝 Agent B – Editor
- Strong rewriting  
- JSON-only output  
- Automatic JSON cleanup  

## 📊 Google Sheets Logging
Logs:
- Timestamp  
- Topic  
- Writer Draft  
- Final Post  
- Tokens  
- Cost  

---

# 🌐 FastAPI REST API

### POST /generate-post

Input:
```json
{"topic":"Your topic"}
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

Docs: http://localhost:8000/docs

---

# 🐳 Docker Support

```bash
docker compose up -d --build
docker compose down
```

---

# 🔄 n8n Workflow File

```
n8n_multi_agent_workflow.json
```

Import in n8n:
- Workflows → Import → Upload

---

# ⚙️ CI/CD – GitHub Actions

Includes:
- Python install & lint  
- Docker image build  
- Docker Hub push  
- Production build verification  
- Optional deploy trigger  

Secrets:
```
DOCKERHUB_USERNAME
DOCKERHUB_TOKEN
GEMINI_API_KEY
GOOGLE_SHEETS_ID
SERVICE_ACCOUNT_JSON
```

Workflow file:
```
.github/workflows/ci-cd.yml
```

---

# 📁 Project Structure

```
multi_agent_gemini/
├── agents/
├── utils/
├── api.py
├── main.py
├── n8n_multi_agent_workflow.json
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
└── README.md
```

---

# 🔧 Installation

```bash
git clone https://github.com/Profy8712/multi-agent-ai-automation.git
cd multi-agent-ai-automation

python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate   # Windows

pip install -r requirements.txt
```

---

# 🔑 Environment Variables

```
GEMINI_API_KEY=YOUR_KEY
GEMINI_MODEL_NAME=models/gemini-2.5-flash

GOOGLE_SHEETS_CREDENTIALS=credentials.json
GOOGLE_SHEETS_ID=YOUR_SPREADSHEET_ID
```

---

# 👤 Author
**Profy8712**  
https://github.com/Profy8712
