from fastapi import APIRouter
from fastapi.responses import HTMLResponse

from app.views.schemas.tester import SendRequest, SendResponse
from app.models.services.http_service import HttpService
from app.views.templates.tester import TESTER_HTML

router = APIRouter(tags=["Tester"])


@router.post(
    "/send",
    response_model=SendResponse,
    summary="Send a webhook to any URL",
)
async def send_webhook(body: SendRequest):
    return await HttpService.send(body)


@router.get("/tester", include_in_schema=False)
async def tester_page():
    return HTMLResponse(TESTER_HTML)
