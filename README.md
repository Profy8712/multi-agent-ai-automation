# Multi‑Agent AI Automation

This project demonstrates a multi‑agent workflow using **Google Gemini**, where two AI agents collaborate to generate, critique, and refine LinkedIn posts.  
The final outputs are automatically logged into **Google Sheets** along with token usage and cost estimation.

---

## 🚀 Features

- **Agent A – Writer**  
  Generates a first‑draft LinkedIn post based on a given topic.

- **Agent B – Editor**  
  Critiques the draft, identifies weaknesses, and produces a polished, high‑impact final version.

- **Google Sheets Logging**  
  Automatically stores:
  - Timestamp  
  - Topic  
  - Writer draft  
  - Final post  
  - Token usage  
  - Cost estimate  

- **Cost Calculation**  
  Based on Google Gemini token pricing.

- **Environment‑based setup**  
  `.env` file used for API keys and configuration.

---

## 📂 Project Structure

```
multi_agent_gemini/
│
├── agents/
│   ├── writer_agent.py        # Agent A logic
│   ├── editor_agent.py        # Agent B logic
│   └── __init__.py
│
├── utils/
│   ├── gemini_client.py       # Gemini model wrapper
│   ├── google_sheets.py       # Google Sheets integration
│   └── __init__.py
│
├── main.py                    # Entry point
├── requirements.txt
├── .env                       # API keys (not committed)
└── README.md
```

---

## 🔧 Installation

### 1. Clone the repository

```
git clone https://github.com/Profy8712/multi-agent-ai-automation.git
cd multi-agent-ai-automation
```

### 2. Create virtual environment

```
python -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate    # Windows
```

### 3. Install dependencies

```
pip install -r requirements.txt
```

---

## 🔑 Environment Variables (.env)

Create a `.env` file:

```
GEMINI_API_KEY=YOUR_KEY
GOOGLE_SERVICE_ACCOUNT_FILE=credentials.json
GOOGLE_SHEETS_ID=YOUR_SHEET_ID
```

---

## ▶️ Run the workflow

```
python main.py
```

You will see:

- Draft post  
- Editor review  
- Final post  
- Token usage  
- Cost estimate  
- Row added to Google Sheets  

---

## 📊 Google Sheets Setup

1. Create a Google Sheet named **multi_agent_linkedin_posts**
2. Add header row:

```
Timestamp | Topic | Draft (Writer) | Final Post (Editor) | Total Tokens | Cost
```

3. Enable Google APIs:
   - Google Sheets API  
   - Google Drive API  

4. Create service account & JSON key
5. Share the Sheet with the service account email

---

## 📌 Notes

- API keys must NOT be committed to GitHub  
- Works on Windows, macOS, Linux  
- Gemini model currently used: **gemini-1.5-flash**  

---

## 🧩 Future Improvements

- Agent C: auto‑posting to LinkedIn  
- Web interface  
- CI/CD automation  
- Docker containerization  

---

## 📄 License

MIT License  
Free for educational and commercial use.

---

## ❤️ Author

Developed by **Profy8712**  
GitHub: https://github.com/Profy8712


