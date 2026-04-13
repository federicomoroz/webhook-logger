from pydantic import BaseModel


class SourceStats(BaseModel):
    source: str
    count: int


class StatsResponse(BaseModel):
    total: int
    by_source: list[SourceStats]
