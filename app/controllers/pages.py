from fastapi import APIRouter, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.repositories.event_repository import EventRepository
from app.views.templates.docs import DOCS_HTML
from app.views.templates.landing import render_landing

router = APIRouter()


@router.get("/", include_in_schema=False)
def landing_page(db: Session = Depends(get_db)):
    rows = EventRepository.get_stats(db)
    total = sum(r.count for r in rows)
    return HTMLResponse(render_landing(rows, total))


@router.get("/docs", include_in_schema=False)
async def docs_page():
    return HTMLResponse(DOCS_HTML)
