# 🤖 AI Text Processing Workflow

**An intelligent, end-to-end automation system that turns raw text into actionable insights — powered by OpenAI, orchestrated by n8n, and delivered straight to your inbox.**

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![n8n](https://img.shields.io/badge/n8n-Automation-EA4B71?logo=n8n&logoColor=white)](https://n8n.io/)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o--mini-412991?logo=openai&logoColor=white)](https://openai.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](#-license)

---

## 📖 Overview

This project demonstrates a **production-style automation pipeline** that collects text (or a URL) from a user, processes it with AI, stores the results, and notifies the user by email — all without manual intervention.

It's built to showcase how a lightweight **FastAPI backend**, a **no-code automation layer (n8n)**, and **OpenAI's language models** can work together to deliver a real, usable product in a matter of hours.

> 💡 **Use case:** Article/document summarization, content triage, research note-taking, customer feedback analysis — anywhere raw text needs to become a clean, structured summary.

---

## 🔄 How It Works

```
┌─────────────┐      ┌──────────────────┐      ┌───────────────┐
│   Frontend   │ ───▶ │  FastAPI Backend  │ ───▶ │  n8n Webhook  │
│ (HTML / JS)  │      │  (Session Mgmt)   │      │               │
└─────────────┘      └──────────────────┘      └───────┬───────┘
                                                          ▼
                                                ┌───────────────────┐
                                                │  OpenAI GPT-4o-mini │
                                                │ Summary + Key Points │
                                                └─────────┬─────────┘
                                                          ▼
                                                ┌───────────────────┐
                                                │   Google Sheets     │
                                                │   (Data Storage)     │
                                                └─────────┬─────────┘
                                                          ▼
                                                ┌───────────────────┐
                                                │   Gmail Notification │
                                                │   (Sent to User)      │
                                                └───────────────────┘
```

1. **User submits** their email and text (or a URL) via the web frontend.
2. **FastAPI backend** validates the input, generates a unique `session_id`, and forwards it to n8n.
3. **n8n workflow** sends the text to **OpenAI (GPT-4o-mini)**, which returns a concise summary and 3 key points.
4. Results are **appended to Google Sheets** for record-keeping.
5. **Gmail** automatically emails the processed results back to the user.

---

## ✨ Key Features

| Feature | Description |
|---|---|
| 🧠 **AI Summarization** | Generates a clear 2–4 sentence summary using GPT-4o-mini |
| 📌 **Key Point Extraction** | Pulls out 3 concise key points from any text |
| 🔗 **URL Support** | Accepts a URL instead of raw text (bonus endpoint) |
| 🗂️ **Automatic Logging** | Every request is saved to Google Sheets with a timestamp |
| 📧 **Instant Notification** | Users get an email the moment processing completes |
| 🆔 **Session Tracking** | Each request gets a unique session ID for traceability |
| ⚡ **Async & Fast** | Built on FastAPI for high-performance, non-blocking requests |

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Frontend** | HTML, CSS, JavaScript |
| **Backend** | Python, FastAPI, Uvicorn |
| **Automation** | n8n Cloud |
| **AI Engine** | OpenAI GPT-4o-mini |
| **Data Storage** | Google Sheets |
| **Notifications** | Gmail (OAuth2) |

---

## 📁 Project Structure

```
project/
├── backend/
│   ├── main.py              # FastAPI application
│   └── requirements.txt     # Python dependencies
├── frontend/
│   └── index.html           # User-facing web interface
├── workflow.json            # Importable n8n workflow definition
└── README.md                # Project documentation
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- An [n8n Cloud](https://app.n8n.cloud) account (or self-hosted instance)
- An OpenAI API key (or n8n's built-in AI credits)
- A Google account (for Sheets + Gmail integration)

### 1️⃣ Backend Setup

```bash
# Navigate to the backend directory
cd backend

# Create a virtual environment
python -m venv venv

# Activate it
source venv/bin/activate       # Mac/Linux
venv\Scripts\activate          # Windows

# Install dependencies
pip install fastapi uvicorn httpx pydantic[email]
```

Update the webhook URL in `main.py`:

```python
N8N_WEBHOOK_URL = "https://your-n8n-instance.app.n8n.cloud/webhook/ai-processor"
```

Start the server:

```bash
uvicorn main:app --reload --port 8000
```

### 2️⃣ Frontend Setup

Open `frontend/index.html` and set the API base URL:

```javascript
const API_BASE = 'http://localhost:8000';
```

Then simply open the file in your browser.

### 3️⃣ n8n Workflow Setup

1. Log in to [n8n Cloud](https://app.n8n.cloud).
2. Go to **Workflows → Import from File** and select `workflow.json`.
3. Connect the required credentials (see below).
4. Click **Publish**, then copy the **Production Webhook URL** into `main.py`.

#### Workflow Nodes

| Node | Purpose |
|---|---|
| Webhook Trigger | Receives data from the FastAPI backend |
| Respond to Webhook | Sends an immediate acknowledgment |
| OpenAI (Message a Model) | Generates the summary and key points |
| Code (JavaScript) | Parses the AI's response |
| Append Row in Sheet | Saves results to Google Sheets |
| Send a Message (Gmail) | Emails the results to the user |

#### Required Credentials

| Service | Setup |
|---|---|
| OpenAI | Connect via n8n ($5 free credit) or your own API key |
| Google Sheets | OAuth2 — sign in with Google |
| Gmail | OAuth2 — sign in with Google |

#### Google Sheet Headers

Create a sheet with these column headers in **Row 1**:

```
Session ID | Email | Original Text | Summary | Key Points | Timestamp
```

---

## 📋 API Reference

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Health check |
| `POST` | `/process` | Submit text for AI processing |
| `POST` | `/process-url` | Submit a URL for AI processing |

### Request Example

```json
{
  "email": "user@example.com",
  "text": "Your text here..."
}
```

### Response Example

```json
{
  "status": "queued",
  "session_id": "ABC123",
  "message": "Your text is being processed."
}
```

---

## 🔧 Troubleshooting

| Problem | Solution |
|---|---|
| CORS error | Confirm the backend is running on port 8000 |
| n8n returns 404 | Make sure the workflow is Active/Published |
| Email not received | Check the spam/junk folder |
| Google Sheets error | Re-authorize the OAuth2 credential |
| OpenAI error | Verify your n8n credit balance or API key |

---

## 🗺️ Roadmap

- [ ] Add support for PDF/document uploads
- [ ] Multi-language summarization
- [ ] Dashboard for viewing processing history
- [ ] Slack/Discord notification option

---

## 📄 License

This project is open-sourced under the [MIT License](LICENSE).

---

## 👤 Author

**Delowar**
n8n Instance: `delowarcse63.app.n8n.cloud`

⭐ If you find this project useful, consider giving it a star!
