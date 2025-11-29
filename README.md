# 📌 Multi-Agent AI Automation  
### Automated LinkedIn Post Generation using Google Gemini + Google Sheets + Python

This project demonstrates a **multi-agent AI workflow** where two specialized agents collaborate to generate and refine professional LinkedIn posts:

- ✍️ **Agent A (Writer)** — generates an initial draft  
- 📝 **Agent B (Editor)** — critiques the draft and rewrites it into a sharper, more impactful version  

The final results, including token usage and cost estimation, are automatically logged into **Google Sheets** via a Google Service Account.

---

## 🚀 Features

### 🤖 Agent A — Writer
Creates a concise, conversational, and professional LinkedIn post based on a given topic. The writer avoids:

- buzzwords  
- emojis  
- hashtags  
- vague or generic statements  

### 🧠 Agent B — Editor
Refines the Writer's draft and returns structured JSON:

```json
{
  "critique": "…",
  "final_post": "…"
}
```

### 📊 Google Sheets Logging
Each workflow run stores:

- Timestamp  
- Topic  
- Draft (Writer)  
- Final Post (Editor)  
- Total Tokens  
- Cost  

### 💰 Cost Calculation
Total tokens × price per token (configurable in `.env`).

### ⚙️ Environment-Based Configuration  
All secrets and configuration are handled using a `.env` file.

---

## 📁 Project Structure

```
multi_agent_gemini/
│
├── agents/
│   ├── writer_agent.py         # Agent A logic
│   ├── editor_agent.py         # Agent B logic
│   └── __init__.py
│
├── utils/
│   ├── gemini_client.py        # Gemini API wrapper
│   ├── google_sheets.py        # Sheets logging
│   └── __init__.py
│
├── main.py                     # Main workflow entry point
├── requirements.txt
├── .env                        # Environment variables (not included in repo)
└── README_EN.md
```

---

## 🔧 Installation

### 1. Clone the repository

```bash
git clone https://github.com/Profy8712/multi-agent-ai-automation.git
cd multi-agent-ai-automation
```

### 2. Create & activate virtual environment

```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate       # macOS/Linux
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Variables (.env)

Create a `.env` file in the project root:

```
GEMINI_API_KEY=YOUR_GEMINI_API_KEY
GEMINI_MODEL_NAME=models/gemini-2.5-flash
TOKEN_PRICE=0.000002

GOOGLE_SHEETS_CREDENTIALS=credentials.json
GOOGLE_SHEETS_ID=YOUR_SPREADSHEET_ID
```

---

## ▶️ Running the Workflow

Run:

```bash
python main.py
```

The script prints:

- Draft (Agent A)  
- Editor critique (Agent B)  
- Final post  
- Token usage  
- Cost  
- Confirmation of Google Sheets logging  

---

## 📊 Setting Up Google Sheets

1. Create a Google Sheet  
2. Add header row:

```
Timestamp | Topic | Draft (Writer) | Final Post (Editor) | Total Tokens | Cost
```

3. Enable:
   - Google Sheets API  
   - Google Drive API  

4. Create a **service account** in Google Cloud  
5. Download `credentials.json`  
6. Share the sheet with the service account email (Editor access)

---

## 🔄 Optional: n8n Integration

An n8n workflow is included:

- Webhook trigger  
- Writer → Editor → Sheets pipeline  
- JSON response  

Import via:  
**n8n → Settings → Import Workflow**

---

## 🧩 Future Enhancements

- Agent C: automatic LinkedIn posting  
- Web dashboard  
- API endpoint  
- Docker support  
- CI/CD automation  

---

## 📄 License

MIT License — free for personal and commercial use.

---

## 👤 Author

**Profy8712**  
GitHub: https://github.com/Profy8712
