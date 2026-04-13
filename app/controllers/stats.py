from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.views.schemas.stats import StatsResponse
from app.models.services.event_service import EventService

router = APIRouter(tags=["Stats"])


@router.get(
    "/stats",
    response_model=StatsResponse,
    summary="Event counts grouped by source",
)
def get_stats(db: Session = Depends(get_db)):
    return EventService.get_stats(db)
