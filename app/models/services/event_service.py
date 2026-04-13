import json
import logging
from typing import Any

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.repositories.event_repository import EventRepository
from app.views.schemas.event import EventCreatedResponse, EventResponse
from app.views.schemas.stats import SourceStats, StatsResponse

logger = logging.getLogger(__name__)

RELEVANT_HEADER_PREFIXES = ("content-type", "user-agent", "x-")


def _filter_headers(headers: dict[str, str]) -> dict[str, str]:
    return {
        k: v
        for k, v in headers.items()
        if k.lower().startswith(RELEVANT_HEADER_PREFIXES)
    }


class EventService:
    @staticmethod
    def create_event(
        db: Session,
        source: str,
        body: Any,
        headers: dict[str, str],
        ip: str,
    ) -> EventCreatedResponse:
        filtered_headers = _filter_headers(headers)
        payload_str = json.dumps(body)
        headers_str = json.dumps(filtered_headers)

        try:
            event = EventRepository.create(db, source, payload_str, headers_str, ip)
        except Exception as exc:
            logger.error("DB error saving event: %s", exc)
            raise HTTPException(status_code=500, detail="Failed to save event.")

        logger.info("Saved event id=%s source=%s ip=%s", event.id, source, ip)
        return EventCreatedResponse(
            id=event.id,
            message=f"Event received and stored (source: {source}).",
        )

    @staticmethod
    def list_events(
        db: Session,
        source: str | None,
        limit: int,
        offset: int,
    ) -> list[EventResponse]:
        events = EventRepository.get_all(db, source=source, limit=limit, offset=offset)
        return [EventResponse.model_validate(e) for e in events]

    @staticmethod
    def get_event(db: Session, event_id: int) -> EventResponse:
        event = EventRepository.get_by_id(db, event_id)
        if not event:
            raise HTTPException(status_code=404, detail=f"Event {event_id} not found.")
        return EventResponse.model_validate(event)

    @staticmethod
    def delete_event(db: Session, event_id: int) -> None:
        event = EventRepository.get_by_id(db, event_id)
        if not event:
            raise HTTPException(status_code=404, detail=f"Event {event_id} not found.")
        EventRepository.delete(db, event)

    @staticmethod
    def get_stats(db: Session) -> StatsResponse:
        rows = EventRepository.get_stats(db)
        total = sum(r.count for r in rows)
        return StatsResponse(
            total=total,
            by_source=[SourceStats(source=r.source, count=r.count) for r in rows],
        )
