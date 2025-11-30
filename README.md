# 🚀 Multi-Agent AI Automation
### Automated LinkedIn Post Generation using Google Gemini + Google Sheets + FastAPI + Docker + CI/CD

This project implements a production-ready **multi-agent AI automation workflow** including:

- 🤖 **Agent A (Writer)** — generates LinkedIn-style content  
- 🧠 **Agent B (Editor)** — critiques and rewrites it in strict JSON  
- 🌐 **FastAPI REST API** — exposes the workflow  
- 📊 **Google Sheets logging**  
- 🐳 **Docker containerization**  
- 🔄 **CI/CD with GitHub Actions + Docker Hub push**

---

# ⭐ Features

### ✍️ Agent A — Writer  
- Generates a clean, concise, buzzword-free LinkedIn draft  
- Includes retry logic for empty Gemini responses  
- Uses Google Gemini API (Flash model)

### 📝 Agent B — Editor  
- Strict editor persona  
- Returns **valid JSON**, always:  
```json
{
  "critique": "...",
  "final_post": "..."
}
```
- Automatically sanitizes malformed outputs  
- Improves clarity, removes buzzwords, sharpens message  

### 📊 Google Sheets Logging  
Each request logs:

- Timestamp  
- Topic  
- Draft  
- Final post  
- Token usage  
- Estimated cost

### 🌐 REST API (FastAPI)
Endpoint:

```
POST /generate-post
```

Example request:
```json
{ "topic": "The future of AI automation" }
```

Swagger UI:  
👉 http://localhost:8000/docs

---

# 📂 Project Structure

```
multi-agent-gemini/
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
├── requirements.txt
├── .env.example
└── README.md
```

---

# 🔧 Local Installation

Clone:

```bash
git clone https://github.com/Profy8712/multi-agent-ai-automation.git
cd multi-agent-ai-automation
```

Create virtual environment:

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

Create a `.env` file:

```
GEMINI_API_KEY=YOUR_GEMINI_KEY
GEMINI_MODEL_NAME=models/gemini-2.5-flash
TOKEN_PRICE=0.000002

GOOGLE_SHEETS_CREDENTIALS=credentials.json
GOOGLE_SHEETS_ID=YOUR_GOOGLE_SHEET_ID
```

Use `.env.example` as a template.

---

# ▶️ Running Locally

Run main script:

```bash
python main.py
```

Run API:

```bash
uvicorn api:app --reload
```

Swagger docs:  
👉 http://127.0.0.1:8000/docs

---

# 🐳 Docker Support

### Start container:

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

# 🐳 Dockerfile Overview

- Python 3.11 slim  
- Installs dependencies  
- Runs FastAPI via Uvicorn  
- Production-ready container  

---

# 🔄 CI/CD (GitHub Actions + Docker Hub)

Workflow file:  
`.github/workflows/ci-cd.yml`

Pipeline steps:

1️⃣ Lint & compile Python code  
2️⃣ Run tests (if any)  
3️⃣ Build Docker image  
4️⃣ Login to Docker Hub  
5️⃣ Push `latest` tag  

### Required GitHub Secrets 🎯

| Secret | Value |
|--------|--------|
| `REGISTRY_USERNAME` | Docker Hub username |
| `REGISTRY_PASSWORD` | Docker Hub Personal Access Token |
| `REGISTRY_REPOSITORY` | profy025/multi-agent-ai-automation |

Trigger:  
- Push to **main**  
- Pull requests to **main**

---

# 📊 Google Sheets Setup

1. Create a new Google Sheet  
2. Add this header row:

```
Timestamp | Topic | Draft | Final Post | Total Tokens | Cost
```

3. Go to Google Cloud Console  
4. Enable:
   - Google Sheets API
   - Google Drive API  
5. Create a **Service Account**  
6. Download `credentials.json`  
7. Share your sheet with the service account email  

---

# 🧩 Technology Stack

- FastAPI  
- Google Gemini API  
- gspread  
- OAuth2 Service Account  
- Docker / Docker Compose  
- GitHub Actions  
- Python 3.11  

---

# 🔮 Future Enhancements

- Agent C (auto LinkedIn posting)  
- Web UI Dashboard  
- Kubernetes deployment  
- Grafana monitoring  
- Rate-limiter & caching  
- OAuth2 authentication  

---

# 👤 Author

**Profy8712**  
👉 https://github.com/Profy8712
