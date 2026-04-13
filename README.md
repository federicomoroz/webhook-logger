# Webhook Logger

A backend service that receives, stores, and exposes webhook events from any source.

Built as a portfolio project to demonstrate: layered architecture, SOLID principles, clean API design, and production deployment.

**Live demo:** https://webhook-logger-9paz.onrender.com

---

## What it does

Any system that emits webhooks — GitHub, Stripe, MercadoLibre, your own app — can point to this service. Every incoming request is validated and persisted with its payload, filtered headers, source IP, and timestamp. A REST API exposes the full event history for auditing or debugging. A built-in tester lets you fire outbound HTTP requests directly from the browser.

---

## Architecture

The project follows **MVC + Repository Pattern** with strict layer separation. Each component has a single responsibility and no layer skips another.

```
┌─────────────────────────────────────────────────────────────┐
│                        HTTP Request                         │
└───────────────────────────┬─────────────────────────────────┘
                            │
┌───────────────────────────▼─────────────────────────────────┐
│                     CONTROLLERS  (C)                        │
│                                                             │
│  webhooks.py   events.py   stats.py   tester.py  pages.py  │
│                                                             │
│  • FastAPI routers — input validation only                  │
│  • Depend-inject DB session via FastAPI Depends()           │
│  • Delegate all logic to the Service layer                  │
└───────────────────────────┬─────────────────────────────────┘
                            │
┌───────────────────────────▼─────────────────────────────────┐
│                       MODELS  (M)                           │
│                                                             │
│         ┌──────────────────────────────────┐               │
│         │           Services               │               │
│         │  event_service.py                │               │
│         │  • Business logic                │               │
│         │  • Header filtering              │               │
│         │  • Error handling (404 / 500)    │               │
│         │  • Raises HTTPException          │               │
│         │                                  │               │
│         │  http_service.py                 │               │
│         │  • Outbound HTTP via httpx        │               │
│         │  • Timeout / error mapping       │               │
│         └──────────────┬───────────────────┘               │
│                        │                                    │
│         ┌──────────────▼───────────────────┐               │
│         │          Repositories            │               │
│         │  event_repository.py             │               │
│         │  • All DB access (SQLAlchemy)     │               │
│         │  • No business logic here        │               │
│         └──────────────┬───────────────────┘               │
│                        │                                    │
│         ┌──────────────▼───────────────────┐               │
│         │            ORM Model             │               │
│         │  event.py  (Event table)         │               │
│         └──────────────────────────────────┘               │
└───────────────────────────┬─────────────────────────────────┘
                            │
┌───────────────────────────▼─────────────────────────────────┐
│                        VIEWS  (V)                           │
│                                                             │
│  schemas/              templates/                           │
│  ├─ event.py           ├─ landing.py   (home page)          │
│  ├─ stats.py           ├─ docs.py      (Swagger UI)         │
│  └─ tester.py          └─ tester.py   (HTTP tester)         │
│                                                             │
│  • Pydantic models for request / response typing            │
│  • field_validator: JSON string → dict at schema boundary   │
│  • Server-side HTML rendering (no framework dependency)     │
└─────────────────────────────────────────────────────────────┘
```

---

## Request flow: receiving a webhook

Step by step, what happens when `POST /webhooks/github` is called:

```
 External system
      │
      │  POST /webhooks/github
      │  Body: { "action": "push", "ref": "refs/heads/main" }
      │
      ▼
 ┌─────────────────────────────────────────────────┐
 │  Controller  (webhooks.py)                      │
 │                                                 │
 │  1. Path param validated: source ≤ 255 chars    │
 │  2. Body parsed: must be valid JSON object      │
 │  3. Client IP extracted from request            │
 │  4. → EventService.create_event(...)            │
 └──────────────────────┬──────────────────────────┘
                        │
                        ▼
 ┌─────────────────────────────────────────────────┐
 │  Service  (event_service.py)                    │
 │                                                 │
 │  5. Headers filtered: keeps only               │
 │     Content-Type, User-Agent, X-* prefixes      │
 │  6. payload and headers serialized to JSON str  │
 │  7. → EventRepository.create(...)               │
 └──────────────────────┬──────────────────────────┘
                        │
                        ▼
 ┌─────────────────────────────────────────────────┐
 │  Repository  (event_repository.py)              │
 │                                                 │
 │  8. SQLAlchemy ORM insert                       │
 │  9. db.commit() + db.refresh()                  │
 │  10. Returns Event ORM object                   │
 └──────────────────────┬──────────────────────────┘
                        │
                        ▼
 ┌─────────────────────────────────────────────────┐
 │  Schema  (EventCreatedResponse)                 │
 │                                                 │
 │  11. Typed response: { id: 42, message: "..." } │
 │  12. FastAPI serializes → HTTP 201 JSON         │
 └─────────────────────────────────────────────────┘
```

---

## SOLID principles applied

| Principle | Where |
|-----------|-------|
| **S** — Single Responsibility | Each class/module does one thing. `EventRepository` only touches the DB. `EventService` only applies business rules. Controllers only handle HTTP. |
| **O** — Open/Closed | Adding a new event source requires zero changes to existing code — just `POST /webhooks/{new_source}`. |
| **L** — Liskov Substitution | `EventRepository` and `HttpService` are pure static-method classes. Any substitute that upholds the same interface works transparently. |
| **I** — Interface Segregation | Controllers import only the service they need. `tester.py` depends on `HttpService`, never on `EventService`. |
| **D** — Dependency Inversion | Controllers never instantiate DB sessions directly. The session is injected via `Depends(get_db)` — the controller depends on the abstraction, not the implementation. |

---

## API reference

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/webhooks/{source}` | Receive a webhook. `source` is a free label (`github`, `stripe`, etc.) |
| `GET` | `/events` | List events. Query params: `source`, `limit` (default 50, max 500), `offset` |
| `GET` | `/events/{id}` | Get a single event by ID |
| `DELETE` | `/events/{id}` | Delete an event |
| `GET` | `/stats` | Event counts grouped by source |
| `POST` | `/send` | Fire an outbound HTTP request to any URL (webhook tester) |
| `GET` | `/tester` | Browser-based HTTP tester UI |
| `GET` | `/docs` | Interactive Swagger UI |

Full interactive documentation at `/docs`.

---

## Data model

```
events
├── id           INTEGER   PRIMARY KEY AUTOINCREMENT
├── source       TEXT      indexed — value of {source} path param
├── payload      TEXT      JSON-serialized request body
├── headers      TEXT      JSON-serialized filtered headers
├── ip           TEXT      caller's IP address
└── received_at  DATETIME  server-side UTC timestamp (auto)
```

Headers stored: `Content-Type`, `User-Agent`, and any `X-*` headers. Host, cookie, and authorization headers are deliberately discarded.

---

## Run locally

```bash
git clone https://github.com/federicomoroz/webhook-logger.git
cd webhook-logger

python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt

uvicorn main:app --reload
# → http://localhost:8000
```

SQLite database is created automatically on first start.

---

## Quick test

```bash
# Send a webhook
curl -X POST http://localhost:8000/webhooks/github \
  -H "Content-Type: application/json" \
  -d '{"action": "push", "ref": "refs/heads/main", "repository": {"name": "my-repo"}}'

# List stored events
curl http://localhost:8000/events

# Filter by source
curl "http://localhost:8000/events?source=github&limit=10"

# Get stats
curl http://localhost:8000/stats

# Delete an event
curl -X DELETE http://localhost:8000/events/1
```

---

## Project structure

```
webhook-logger/
├── main.py                              # Entry point for uvicorn
├── app/
│   ├── main.py                          # App factory (FastAPI instance, middleware, routers)
│   ├── core/
│   │   └── database.py                  # SQLAlchemy engine, session, Depends(get_db)
│   ├── models/                          # M — business logic and data
│   │   ├── event.py                     # ORM model
│   │   ├── repositories/
│   │   │   └── event_repository.py      # All DB queries
│   │   └── services/
│   │       ├── event_service.py         # Webhook business rules
│   │       └── http_service.py          # Outbound HTTP (httpx)
│   ├── views/                           # V — presentation layer
│   │   ├── schemas/
│   │   │   ├── event.py                 # Request / response Pydantic models
│   │   │   ├── stats.py
│   │   │   └── tester.py
│   │   └── templates/
│   │       ├── landing.py               # Home page HTML
│   │       ├── docs.py                  # Custom Swagger UI page
│   │       └── tester.py                # HTTP tester page
│   └── controllers/                     # C — HTTP routing
│       ├── webhooks.py                  # POST /webhooks/{source}
│       ├── events.py                    # GET|DELETE /events
│       ├── stats.py                     # GET /stats
│       ├── tester.py                    # POST /send, GET /tester
│       └── pages.py                     # GET /, GET /docs
├── static/
│   ├── terminal.css                     # Custom Swagger UI theme
│   └── favicon.svg
├── requirements.txt
└── render.yaml                          # Render deploy config
```

---

## Stack

- **Python 3.11** + **FastAPI** — typed, async, auto-documented
- **SQLAlchemy 2.0** + **SQLite** — ORM with repository pattern, zero external dependency
- **Pydantic v2** — schema validation and response serialization
- **httpx** — async HTTP client for outbound requests
- **Uvicorn** — ASGI server
- **Render** — free-tier cloud deployment

---

## Deploy on Render

1. Fork this repo
2. Create a **Web Service** on [Render](https://render.com) and connect the repo
3. Render reads `render.yaml` automatically — click **Deploy**

Start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
