# Webhook Logger

A lightweight backend service that receives, stores, and exposes webhook events from any source — built to demonstrate real backend skills: API design, data modeling, error handling, and cloud deployment.

**Live demo:** `https://webhook-logger-xxxx.onrender.com/docs`

---

## What it does

Any system that emits webhooks (GitHub, Stripe, MercadoLibre, your own app) can point to this service. Every incoming request is validated and persisted with its payload, relevant headers, source IP, and timestamp. A REST API exposes the full event history for auditing or debugging.

---

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/webhooks/{source}` | Receive a webhook — `source` is a free label (e.g. `github`, `stripe`) |
| `GET` | `/events` | List events — query params: `source`, `limit` (default 50), `offset` |
| `GET` | `/events/{id}` | Get a single event by ID |
| `DELETE` | `/events/{id}` | Delete an event |
| `GET` | `/stats` | Event counts grouped by source |

Full interactive docs at `/docs` (Swagger UI).

---

## Run locally

```bash
# 1. Clone and enter the project
git clone https://github.com/your-username/webhook-logger.git
cd webhook-logger

# 2. Create a virtual environment and install dependencies
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# 3. Start the server
uvicorn main:app --reload

# 4. Open the docs
open http://localhost:8000/docs
```

SQLite database (`webhook_logger.db`) is created automatically on first run.

---

## Quick test with curl

```bash
# Send a test webhook
curl -X POST http://localhost:8000/webhooks/github \
  -H "Content-Type: application/json" \
  -d '{"action": "push", "ref": "refs/heads/main", "repository": {"name": "my-repo"}}'

# List all events
curl http://localhost:8000/events

# Filter by source
curl "http://localhost:8000/events?source=github&limit=10"

# Get stats
curl http://localhost:8000/stats

# Delete an event
curl -X DELETE http://localhost:8000/events/1
```

---

## Stack

- **Python 3.11** + **FastAPI** — typed, async, auto-documented
- **SQLAlchemy 2.0** + **SQLite** — zero-dependency persistence
- **Uvicorn** — ASGI server
- **Render** — free cloud deployment

---

## Deploy on Render

1. Fork this repo
2. Create a new **Web Service** on [Render](https://render.com), connect the repo
3. Render auto-detects `render.yaml` — just click **Deploy**
4. The SQLite database is created on first start

---

## Project structure

```
webhook-logger/
├── main.py          # FastAPI app + all routes
├── database.py      # SQLAlchemy engine + session factory
├── models.py        # Event ORM model
├── schemas.py       # Pydantic request/response schemas
├── requirements.txt
├── render.yaml      # Render deploy config
└── README.md
```
