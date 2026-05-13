# AI Text Processing Workflow 🤖

A full-stack AI-powered system that collects text from users, processes it with OpenAI, stores results in Google Sheets, and sends email notifications.

---

## 📁 Project Structure

```
project/
├── backend/
│   ├── main.py              # FastAPI backend
│   └── requirements.txt     # Python dependencies
├── frontend/
│   └── index.html           # Frontend UI
├── workflow.json            # n8n workflow export
└── README.md
```

---

## 🔄 System Flow

```
User (Browser)
      ↓
FastAPI Backend  →  Generates session_id
      ↓
n8n Webhook
      ↓
OpenAI (GPT-4o-mini)  →  Summary + Key Points
      ↓
Google Sheets  →  Stores all data
      ↓
Gmail  →  Sends email to user
```

---

## ⚙️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend | HTML, CSS, JavaScript |
| Backend | Python, FastAPI |
| Automation | n8n Cloud |
| AI | OpenAI GPT-4o-mini |
| Storage | Google Sheets |
| Email | Gmail |

---

## 🚀 Setup Guide

### 1. Backend Setup

```bash
# Go to backend folder
cd backend

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Mac/Linux)
source venv/bin/activate

# Install packages
pip install fastapi uvicorn httpx pydantic[email]
```

**Update `main.py`:**
```python
N8N_WEBHOOK_URL = "https://your-n8n-instance.app.n8n.cloud/webhook/ai-processor"
```

**Run server:**
```bash
uvicorn main:app --reload --port 8000
```

---

### 2. Frontend Setup

- Open `frontend/index.html` in browser
- Update API URL in the file:
```js
const API_BASE = 'http://localhost:8000';
```

---

### 3. n8n Workflow Setup

#### Import Workflow
1. Login to [n8n Cloud](https://app.n8n.cloud)
2. Workflows → Import from file → select `workflow.json`
3. Save

#### Nodes in Workflow
| Node | Purpose |
|---|---|
| Webhook Trigger | Receives data from FastAPI |
| Respond to Webhook | Sends immediate response |
| OpenAI (Message a Model) | Generates summary + key points |
| Code in JavaScript | Parses AI response |
| Append row in sheet | Saves to Google Sheets |
| Send a message (Gmail) | Sends email to user |

#### Credentials Required
| Service | How to Connect |
|---|---|
| OpenAI | n8n Connect ($5 free) or own API key |
| Google Sheets | OAuth2 → Sign in with Google |
| Gmail | OAuth2 → Sign in with Google |

#### Google Sheet Headers
Create a sheet with these headers in Row 1:
```
Session ID | Email | Original Text | Summary | Key Points | Timestamp
```

#### Activate Workflow
1. Click **Publish** in n8n
2. Copy **Production URL** from Webhook node
3. Paste URL in `main.py`

---

## 📋 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Health check |
| POST | `/process` | Process text input |
| POST | `/process-url` | Process URL (Bonus) |

### Request Body
```json
{
  "email": "user@example.com",
  "text": "Your text here..."
}
```

### Response
```json
{
  "status": "queued",
  "session_id": "ABC123",
  "message": "Your text is being processed."
}
```

---

## ✨ Features

- ✅ User submits email + text
- ✅ Unique session ID generated
- ✅ AI generates 2-4 sentence summary
- ✅ AI extracts 3 key points
- ✅ Results saved to Google Sheets
- ✅ Email sent to user with results
- ✅ Bonus: Submit URL instead of text

---

## 🔧 Troubleshooting

| Problem | Solution |
|---|---|
| CORS error | Make sure backend is running on port 8000 |
| n8n 404 error | Make sure workflow is Active/Published |
| Email not received | Check spam folder |
| Google Sheets error | Re-authorize OAuth2 credential |
| OpenAI error | Check n8n Connect balance |

---

## 📹 Demo Video

[Watch Demo Video](#)

---

## 👤 Author

- **Name:** Delowar
- **n8n Instance:** delowarcse63.app.n8n.cloud
- **Project:** AI Text Processing Workflow Assignment