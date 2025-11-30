# 🚀 Multi-Agent AI Automation
### Automated LinkedIn Post Generator using Google Gemini + Google Sheets + FastAPI + Docker + CI/CD

This project implements a **production-grade multi-agent AI workflow** with:
- 🤖 **Agent A — Writer** (generates LinkedIn post draft)
- 🧠 **Agent B — Editor** (critiques and rewrites in strict JSON)
- 🌐 **FastAPI REST API**
- 📊 **Google Sheets logging**
- 🐳 **Docker / Docker Compose**
- 🔄 **CI/CD via GitHub Actions + Docker Hub**
- 🛡 **Robust error handling** (detailed below)

---

# ⭐ Features

### ✍️ Agent A — Writer  
- Generates clean, concrete, business-style drafts  
- Avoids buzzwords, emojis, vague statements  
- Retries automatically if Gemini returns empty/blocked content  

### 🧠 Agent B — Editor  
- Returns strict JSON:  
```json
{
  "critique": "...",
  "final_post": "..."
}
```
- Removes buzzwords, sharpens message  
- Automatically fixes malformed JSON returned by Gemini  
- Protects against unexpected editor output  

### 🌐 FastAPI REST API  
Main endpoint:

```
POST /generate-post
```

Request:
```json
{ "topic": "Your topic here" }
```

Response includes:
- writer draft  
- editor critique  
- final edited post  
- token usage  
- cost  

Docs: 👉 http://localhost:8000/docs

### 📊 Google Sheets Logging  
Every request is stored:
- Timestamp  
- Topic  
- Draft  
- Final post  
- Tokens  
- Cost  

### 🐳 Docker Support  
Run entire service in an isolated container.

### 🔄 CI/CD  
Automatic:
- Tests  
- Docker build  
- Docker Hub push  

---

# 🛡 🛡 🛡 **ERROR HANDLING (FULL, DETAILED, PRODUCTION-GRADE)**

The project includes **multi-layer error protection** to ensure reliability.

---

# 1️⃣ Gemini API Error Handling

### ✔️ Case: Gemini returns empty response  
Gemini sometimes returns 0 tokens (blocked content/safety flags).  
Writer agent handles this with **retries + fallback**:

```python
for _ in range(3):
    try:
        text, usage, _ = generate_text(prompt)
        if text.strip():
            return {...}
    except GeminiAPIError:
        last_error = exc
```

After 3 failures:

- fallback draft is returned  
- execution **does not crash**  
- error is logged  

---

### ✔️ Case: Gemini API connectivity failure

Handled in `gemini_client.py`:

```python
except Exception as exc:
    raise GeminiAPIError(f"Gemini API request failed: {exc}")
```

The rest of the app receives a controlled exception.

---

### ✔️ Case: response has no .text field  
Gemini sometimes returns candidates without `.text`.  
We reconstruct text manually:

```python
for cand in response.candidates:
    for part in cand.content.parts:
        if part.text:
            parts.append(part.text)
```

If still empty → **error raised intentionally**:

```python
raise GeminiAPIError("Gemini returned an empty response.")
```

---

# 2️⃣ Editor JSON Parsing Errors

Gemini sometimes returns invalid JSON.

Example of malformed model output:

```
{
  "critique": "..."
  "final_post": ...
```

Editor handles this via:

```python
try:
    payload = json.loads(cleaned)
except Exception:
    critique = f"Failed to parse JSON from editor. Raw response: {cleaned}"
```

In worst-case:
- critique explains the failure  
- original draft is preserved  
- service continues running  

---

# 3️⃣ Google Sheets Logging Errors

If Google Sheets fails (e.g., invalid credentials, rate limits, API outage):

```python
except GoogleSheetsError as exc:
    print("[WARNING] Failed to write data to Google Sheets.")
```

⚠️ Importantly:  
**The post generation STILL succeeds.**  
Sheets logging is optional—not critical.

---

# 4️⃣ FastAPI Error Handling

### ✔️ Invalid request  
Handled automatically by Pydantic → 422 Unprocessable Entity

### ✔️ Gemini error  
Returned as structured 500:

```json
{
  "detail": "Gemini failed: <error>"
}
```

### ✔️ Sheets error  
Returned as 503:

```json
{
  "detail": "Google Sheets is unavailable"
}
```

The API never exposes raw tracebacks.

---

# 5️⃣ Docker Runtime Error Isolation

Docker ensures:

- environment consistency  
- no dependency conflicts  
- API always starts cleanly  
- logs are isolated  

If the container fails → systemd / Docker restart policies can be added.

---

# 6️⃣ CI/CD Error Handling

GitHub Actions pipeline includes:

- syntax check (compileall)
- pip install validation
- Docker registry authentication verification
- safe repository name sanitization (`tr -d '[:space:]'`)
- conditional push only on `main`

Broken builds never reach production.

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

# 🔧 Installation

```bash
git clone https://github.com/Profy8712/multi-agent-ai-automation.git
cd multi-agent-ai-automation
```

Create venv:

```bash
python -m venv venv
source venv/bin/activate
# Windows:
# venv\Scripts\activate
```

Install:

```bash
pip install -r requirements.txt
```

---

# 🔑 Environment Variables

Create `.env`:

```
GEMINI_API_KEY=YOUR_KEY
GEMINI_MODEL_NAME=models/gemini-2.5-flash
TOKEN_PRICE=0.000002

GOOGLE_SHEETS_CREDENTIALS=credentials.json
GOOGLE_SHEETS_ID=YOUR_SHEET_ID
```

---

# 🌐 Start API

```bash
uvicorn api:app --reload
```

Docs:  
👉 http://localhost:8000/docs

---

# 🐳 Docker

Run:

```bash
docker compose up -d --build
```

Stop:

```bash
docker compose down
```

---

# 🔄 CI/CD

Pipeline file: `.github/workflows/ci-cd.yml`

Secrets required:

| Secret | Value |
|--------|--------|
| `REGISTRY_USERNAME` | Docker Hub username |
| `REGISTRY_PASSWORD` | Docker Hub token |
| `REGISTRY_REPOSITORY` | profy025/multi-agent-ai-automation |

Workflow on push to `main`:

- syntax check  
- build docker image  
- push to Docker Hub  

---

# 👤 Author

**Profy8712**  
https://github.com/Profy8712
