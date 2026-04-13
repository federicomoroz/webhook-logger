from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, Path, Request
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.views.schemas.event import EventCreatedResponse
from app.models.services.event_service import EventService

router = APIRouter(prefix="/webhooks", tags=["Webhooks"])


@router.post(
    "/{source}",
    response_model=EventCreatedResponse,
    status_code=201,
    summary="Receive a webhook",
)
async def receive_webhook(
    source: Annotated[str, Path(max_length=255)],
    request: Request,
    db: Session = Depends(get_db),
):
    try:
        body: Any = await request.json()
    except Exception:
        raise HTTPException(status_code=422, detail="Request body must be valid JSON.")

    if not isinstance(body, dict):
        raise HTTPException(status_code=422, detail="Payload must be a JSON object.")

    client_ip = request.client.host if request.client else "unknown"
    return EventService.create_event(db, source, body, dict(request.headers), client_ip)
