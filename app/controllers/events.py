from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.views.schemas.event import EventResponse
from app.models.services.event_service import EventService

router = APIRouter(prefix="/events", tags=["Events"])


@router.get(
    "",
    response_model=list[EventResponse],
    summary="List events",
)
def list_events(
    source: str | None = Query(default=None, description="Filter by source"),
    limit: int = Query(default=50, ge=1, le=500),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
):
    return EventService.list_events(db, source=source, limit=limit, offset=offset)


@router.get(
    "/{event_id}",
    response_model=EventResponse,
    summary="Get event by ID",
)
def get_event(event_id: int, db: Session = Depends(get_db)):
    return EventService.get_event(db, event_id)


@router.delete(
    "/{event_id}",
    status_code=204,
    summary="Delete event by ID",
)
def delete_event(event_id: int, db: Session = Depends(get_db)):
    EventService.delete_event(db, event_id)
