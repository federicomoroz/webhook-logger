from typing import Any
from pydantic import BaseModel


class SendRequest(BaseModel):
    url: str
    payload: dict[str, Any] = {}
    method: str = "POST"
    headers: dict[str, str] = {}


class SendResponse(BaseModel):
    status_code: int
    body: str
    elapsed_ms: float
    ok: bool
