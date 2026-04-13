import json
import logging
from typing import Any

from fastapi import FastAPI, Depends, HTTPException, Request, Query
from sqlalchemy import func, text
from sqlalchemy.orm import Session

import models
import schemas
from database import Base, engine, get_db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Webhook Logger",
    description=(
        "A backend service that receives, stores, and exposes webhook events "
        "from any source. Useful for auditing integrations with GitHub, Stripe, "
        "MercadoLibre, or any custom system."
    ),
    version="1.0.0",
)

RELEVANT_HEADER_PREFIXES = ("content-type", "user-agent", "x-")


def _filter_headers(headers: dict[str, str]) -> dict[str, str]:
    return {
        k: v
        for k, v in headers.items()
        if k.lower().startswith(RELEVANT_HEADER_PREFIXES)
    }


@app.post(
    "/webhooks/{source}",
    response_model=schemas.EventCreatedResponse,
    status_code=201,
    summary="Receive a webhook",
    tags=["Webhooks"],
)
async def receive_webhook(
    source: str,
    request: Request,
    db: Session = Depends(get_db),
):
    try:
        body: Any = await request.json()
    except Exception:
        raise HTTPException(
            status_code=422,
            detail="Request body must be valid JSON.",
        )

    if not isinstance(body, dict):
        raise HTTPException(
            status_code=422,
            detail="Payload must be a JSON object.",
        )

    client_ip = request.client.host if request.client else "unknown"
    filtered_headers = _filter_headers(dict(request.headers))

    event = models.Event(
        source=source,
        payload=json.dumps(body),
        headers=json.dumps(filtered_headers),
        ip=client_ip,
    )
    db.add(event)
    try:
        db.commit()
        db.refresh(event)
    except Exception as exc:
        db.rollback()
        logger.error("DB error saving event: %s", exc)
        raise HTTPException(status_code=500, detail="Failed to save event.")

    logger.info("Saved event id=%s source=%s ip=%s", event.id, source, client_ip)
    return schemas.EventCreatedResponse(
        id=event.id,
        message=f"Event received and stored (source: {source}).",
    )


@app.get(
    "/events",
    response_model=list[schemas.EventResponse],
    summary="List events",
    tags=["Events"],
)
def list_events(
    source: str | None = Query(default=None, description="Filter by source"),
    limit: int = Query(default=50, ge=1, le=500, description="Max results"),
    offset: int = Query(default=0, ge=0, description="Pagination offset"),
    db: Session = Depends(get_db),
):
    query = db.query(models.Event)
    if source:
        query = query.filter(models.Event.source == source)
    return (
        query.order_by(models.Event.received_at.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )


@app.get(
    "/events/{event_id}",
    response_model=schemas.EventResponse,
    summary="Get event by ID",
    tags=["Events"],
)
def get_event(event_id: int, db: Session = Depends(get_db)):
    event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail=f"Event {event_id} not found.")
    return event


@app.delete(
    "/events/{event_id}",
    status_code=204,
    summary="Delete event by ID",
    tags=["Events"],
)
def delete_event(event_id: int, db: Session = Depends(get_db)):
    event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail=f"Event {event_id} not found.")
    db.delete(event)
    db.commit()


@app.get(
    "/stats",
    response_model=schemas.StatsResponse,
    summary="Event counts grouped by source",
    tags=["Stats"],
)
def get_stats(db: Session = Depends(get_db)):
    rows = (
        db.query(models.Event.source, func.count(models.Event.id).label("count"))
        .group_by(models.Event.source)
        .order_by(text("count DESC"))
        .all()
    )
    total = sum(r.count for r in rows)
    return schemas.StatsResponse(
        total=total,
        by_source=[schemas.SourceStats(source=r.source, count=r.count) for r in rows],
    )
