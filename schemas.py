import json
from datetime import datetime, timezone
from typing import Any
from pydantic import BaseModel, field_validator


class EventCreate(BaseModel):
    source: str
    payload: dict[str, Any]
    headers: dict[str, str]
    ip: str


class EventResponse(BaseModel):
    id: int
    source: str
    payload: dict[str, Any]
    headers: dict[str, Any]
    ip: str
    received_at: datetime

    model_config = {"from_attributes": True}

    @field_validator("payload", "headers", mode="before")
    @classmethod
    def parse_json_str(cls, v: Any) -> Any:
        if isinstance(v, str):
            return json.loads(v)
        return v

    @field_validator("received_at", mode="before")
    @classmethod
    def assume_utc(cls, v: Any) -> Any:
        if isinstance(v, datetime) and v.tzinfo is None:
            return v.replace(tzinfo=timezone.utc)
        return v


class EventCreatedResponse(BaseModel):
    id: int
    message: str


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


class SourceStats(BaseModel):
    source: str
    count: int


class StatsResponse(BaseModel):
    total: int
    by_source: list[SourceStats]
