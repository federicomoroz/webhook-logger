from datetime import datetime
from typing import Any
from pydantic import BaseModel


class EventCreate(BaseModel):
    source: str
    payload: dict[str, Any]
    headers: dict[str, str]
    ip: str


class EventResponse(BaseModel):
    id: int
    source: str
    payload: str
    headers: str
    ip: str
    received_at: datetime

    model_config = {"from_attributes": True}


class EventCreatedResponse(BaseModel):
    id: int
    message: str


class SourceStats(BaseModel):
    source: str
    count: int


class StatsResponse(BaseModel):
    total: int
    by_source: list[SourceStats]
