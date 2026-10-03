from pydantic import BaseModel, Field, model_validator

from app.constants import WALK_LINK_M
from app.schemas.common import Point, PointBase

class JourneyRequest(BaseModel):
    origin: Point | None = None
    origin_stop_id: int | None = None
    destination: Point | None = None
    destination_stop_id: int | None = None
    max_walk_m: int = Field(800, ge=50, le=3000, description="max walk from/to the given coordinates")
    transfer_walk_m: int = Field(300, ge=0, le=WALK_LINK_M, description="max walk between stops when transferring")
    board_penalty_s: int = Field(120, ge=0, description="cost of each boarding; raise it to avoid transfers")

    @model_validator(mode="after")
    def _exactly_one(self):
        if (self.origin is None) == (self.origin_stop_id is None):
            raise ValueError("provide exactly one of origin / origin_stop_id")
        if (self.destination is None) == (self.destination_stop_id is None):
            raise ValueError("provide exactly one of destination / destination_stop_id")
        return self

class PathPoint(PointBase):
    name: str | None = None
    stop_id: int | None = None
    seq: int | None = None

class BusInfo(BaseModel):
    route_id: int
    route_code: str
    route_name: str | None
    pattern_id: int
    headsign: str | None
    direction: int
    board_stop: PathPoint
    alight_stop: PathPoint
    stops_passed: list[PathPoint]  # intermediate stops, excluding board/alight
    num_stops: int
    est_wait_s: int

class Leg(BaseModel):
    mode: str  # "walk" | "bus"
    instruction: str
    start: PathPoint
    end: PathPoint
    duration_s: int
    distance_m: float  # straight-line for walking; summed stop-to-stop for bus
    points: list[PathPoint]
    bus: BusInfo | None = None

class JourneySummary(BaseModel):
    total_duration_s: int
    walking_m: float
    num_buses: int
    num_transfers: int

class JourneyResponse(BaseModel):
    summary: JourneySummary
    legs: list[Leg]
    geojson: dict
