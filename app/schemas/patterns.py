from pydantic import BaseModel, Field

from app.schemas.stops import StopOut

class PatternStopIn(BaseModel):
    stop_id: int
    offset_seconds: int | None = None

class PatternIn(BaseModel):
    direction: int = 0
    headsign: str | None = None
    name: str | None = None
    osm_relation_id: int | None = None
    stops: list[PatternStopIn] = []  # in travel order; seq is assigned 1..n

class PatternStopAdd(BaseModel):
    stop_id: int
    seq: int | None = Field(None, ge=1)  # omit to append at the end
    offset_seconds: int | None = None

class PatternStopOut(BaseModel):
    seq: int
    offset_seconds: int | None = None
    stop: StopOut

class PatternOut(BaseModel):
    id: int
    route_id: int
    direction: int
    headsign: str | None = None
    name: str | None = None
    osm_relation_id: int | None = None
    stops: list[PatternStopOut] = []
