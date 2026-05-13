import os
import re
import uuid
from typing import Dict, Union

import requests
from bs4 import BeautifulSoup
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr, Field
from dotenv import load_dotenv


def get_setting(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Environment variable {name} must be set")
    return value


load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"), override=True)
N8N_WEBHOOK_URL = os.getenv("N8N_WEBHOOK_URL")
print(f"Loaded N8N_WEBHOOK_URL: {N8N_WEBHOOK_URL}")


def ensure_n8n_webhook_url() -> str:
    if not N8N_WEBHOOK_URL:
        raise HTTPException(
            status_code=500,
            detail=(
                "N8N_WEBHOOK_URL is not configured. "
                "Set it in backend/.env or as an environment variable."
            ),
        )
    return N8N_WEBHOOK_URL

app = FastAPI(
    title="AI Text Processing Backend",
    description="Receives email and text or URL, generates session_id, and forwards payload to n8n webhook.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class ProcessRequest(BaseModel):
    email: EmailStr
    text: str = Field(default="", description="Plain text input")
    url: str = Field(default="", description="Optional URL to scrape")


class ProcessResponse(BaseModel):
    session_id: str
    forwarded_to_n8n: bool
    n8n_status_code: int
    n8n_response: Union[Dict, str]


def scrape_page_text(url: str) -> str:
    """Scrape visible text from a web page and clean it."""
    try:
        response = requests.get(url, timeout=15, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()
    except requests.RequestException as exc:
        raise HTTPException(status_code=400, detail=f"Unable to fetch URL: {exc}")

    soup = BeautifulSoup(response.text, "html.parser")
    for tag in soup(["script", "style", "noscript"]):
        tag.extract()

    text = soup.get_text(separator="\n")
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    cleaned = " ".join(lines)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()

    if len(cleaned) < 20:
        raise HTTPException(status_code=400, detail="Scraped content is too short to process.")

    return cleaned


@app.get("/health")
async def health() -> Dict[str, str]:
    return {"status": "ok"}


@app.post("/process", response_model=ProcessResponse)
async def process_request(request: ProcessRequest) -> ProcessResponse:
    text_value = request.text.strip()
    if request.url and not text_value:
        text_value = scrape_page_text(request.url)

    if not text_value:
        raise HTTPException(status_code=400, detail="Text or URL content is required.")

    session_id = uuid.uuid4().hex
    payload = {
        "email": request.email,
        "text": text_value,
        "session_id": session_id,
    }

    n8n_url = ensure_n8n_webhook_url()
    print(f"Sending payload to n8n URL: {n8n_url}")
    try:
        response = requests.post(n8n_url, json=payload, timeout=30)
        response.raise_for_status()
        n8n_body = response.json() if response.headers.get("Content-Type", "").startswith("application/json") else response.text
    except requests.RequestException as exc:
        raise HTTPException(status_code=502, detail=f"Failed to send payload to n8n: {exc}")

    return ProcessResponse(
        session_id=session_id,
        forwarded_to_n8n=True,
        n8n_status_code=response.status_code,
        n8n_response=n8n_body,
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
