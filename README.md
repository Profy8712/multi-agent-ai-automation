# 🚀 Multi-Agent AI Automation
### Automated LinkedIn Post Generation using Google Gemini + Google Sheets + FastAPI + Docker + n8n

This repository contains a production-grade multi-agent automation system built to solve the Technical Test Task: Multi-Agent AI Automation and expanded into a full-scale, professional automation project.

The solution integrates:
- Google Gemini AI (Writer Agent + Editor Agent)
- n8n workflow automation
- Google Sheets logging (via Service Account)
- FastAPI REST microservice
- Docker containerization
- GitHub Actions CI/CD pipeline

It demonstrates real-world automation skills: AI orchestration, error handling, structured output validation, token & cost analytics, persistent logging, and deployment readiness.

## 🔥 Technical Test Solution Summary

### 🎯 Objective
Build a workflow where:
1. Agent A (Writer) generates a LinkedIn-style draft.
2. Agent B (Editor) critiques & rewrites it in a punchier tone.
3. System logs results + tokens + cost to Google Sheets.
4. Workflow triggered via Webhook.

## 🧩 Workflow Summary (n8n)

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
{"critique":"...","final_post":"..."}

## 📘 Technical Test Instructions (Included in README)

### 📌 1. Summary of the Task
- Webhook receives: { "topic": "..." }
- Agent A writes the LinkedIn draft.
- Agent B critiques the draft and returns JSON.
- Workflow stores all results in Google Sheets.

### 📌 2. How to Import the Workflow in n8n
1. Open n8n
2. Go to Workflows → Import
3. Upload: n8n_multi_agent_workflow.json
4. Configure credentials:
   - Gemini API Key
   - Google Sheets (Service Account)
5. Activate workflow

### 📌 3. How to Test the Workflow
Run workflow in test mode:

curl -X POST 'https://your-workspace.n8n.cloud/webhook-test/multi-agent-linkedin-post' \
  -H 'Content-Type: application/json' \
  -d '{"topic": "The future of AI Agents in Business"}'

Check:
- Writer output  
- Editor JSON  
- Token calculation  
- Google Sheets row

### 📌 4. Token Usage & Cost Calculation
Gemini fields:
- promptTokenCount  
- totalTokenCount  

Output tokens = totalTokenCount - promptTokenCount

Pricing example:
- Writer: $0.00035 input / $0.00070 output  
- Editor: $0.00350 input / $0.01050 output  

Cost formula:
(tokens_input/1000 × price_input) + (tokens_output/1000 × price_output)

## 🛡 Error Handling
- Empty Writer response → retry  
- Malformed JSON → cleanup  
- Oversized drafts → trimming  
- Sheets write failure → fallback  
- Missing topic → stop workflow  

## 🌐 FastAPI REST API

Endpoint:
POST /generate-post

Input:
{"topic":"Your topic"}

Output:
{
  "draft": "...",
  "critique": "...",
  "final_post": "...",
  "tokens": 123,
  "cost": 0.000246
}

Docs:
http://localhost:8000/docs

## 🐳 Docker Support
docker compose up -d --build  
docker compose down  

## 🔄 n8n Workflow File
File: n8n_multi_agent_workflow.json  
Import through n8n → Workflows → Import  

## ⚙️ CI/CD – GitHub Actions
Includes:
- Python validation  
- Docker build  
- Push to Docker Hub  
- Deploy trigger  

Secrets:
DOCKERHUB_USERNAME  
DOCKERHUB_TOKEN  
GEMINI_API_KEY  
GOOGLE_SHEETS_ID  
SERVICE_ACCOUNT_JSON  

## 📁 Project Structure
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

## 🔧 Installation
git clone https://github.com/Profy8712/multi-agent-ai-automation.git
cd multi-agent-ai-automation

python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

## 🔑 Environment Variables
GEMINI_API_KEY=YOUR_KEY  
GEMINI_MODEL_NAME=models/gemini-2.5-flash  
GOOGLE_SHEETS_CREDENTIALS=credentials.json  
GOOGLE_SHEETS_ID=YOUR_SPREADSHEET_ID  

## 👤 Author
Profy8712  
https://github.com/Profy8712
