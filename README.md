# 📌 Multi-Agent AI Automation  
### Automated LinkedIn Post Generation using Google Gemini + Google Sheets + Python

This project demonstrates a **multi-agent AI workflow** where two specialized agents collaborate to generate and refine professional LinkedIn posts:

- ✍️ **Agent A (Writer)** — generates an initial draft  
- 📝 **Agent B (Editor)** — critiques the draft and rewrites it into a sharper, more impactful version  

The final results, including token usage and estimated cost, are automatically logged into **Google Sheets** using a Google Service Account.

---

## 🚀 Features

### 🤖 Agent A — Writer
Generates a professional LinkedIn-style post based on a given topic.

The writer avoids:
- buzzwords  
- emojis  
- hashtags  
- vague or generic statements  

### 🧠 Agent B — Editor
Refines the Writer's draft and returns structured JSON:

```json
{
  "critique": "...",
  "final_post": "..."
}
```

### 📊 Google Sheets Logging  
Each workflow run stores:

- Timestamp  
- Topic  
- Draft (Writer)  
- Final Post (Editor)  
- Total Tokens  
- Estimated Cost  

### 💰 Cost Calculation  
Uses:  
`total_tokens × TOKEN_PRICE` (configurable in `.env`).

### ⚙️ Environment-Based Configuration  
All secrets and configuration are managed via a `.env` file.

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
├── .env.example                # Configuration template
└── README.md                   # Documentation
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
source venv/bin/activate     # macOS / Linux
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

- Writer Draft  
- Editor Critique  
- Editor Final Post  
- Token usage  
- Estimated cost  
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

4. Create a **Service Account** in Google Cloud  
5. Download `credentials.json`  
6. Share the sheet with your Service Account email (Editor access)

---

## 🔄 Optional: n8n Integration

An optional n8n workflow is included featuring:

- Webhook trigger  
- Writer → Editor → Google Sheets pipeline  
- JSON API response  

Import via:  
**n8n → Settings → Import Workflow**

---

## 🧩 Future Enhancements

- Agent C: automatic LinkedIn posting  
- Web dashboard  
- REST API endpoint  
- Docker containerization  
- CI/CD automation  
- Error reporting dashboard  

---

## 📄 License

MIT License — free for personal and commercial use.

---

## 👤 Author

**Profy8712**  
GitHub: https://github.com/Profy8712
