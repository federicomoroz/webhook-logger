import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.core.database import Base, engine
from app.controllers import events, pages, stats, tester, webhooks

logging.basicConfig(level=logging.INFO)

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Webhook Logger",
    description=(
        "A backend service that receives, stores, and exposes webhook events "
        "from any source. Useful for auditing integrations with GitHub, Stripe, "
        "MercadoLibre, or any custom system."
    ),
    version="1.0.0",
    docs_url=None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST", "DELETE"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

for router in [pages.router, webhooks.router, events.router, stats.router, tester.router]:
    app.include_router(router)
