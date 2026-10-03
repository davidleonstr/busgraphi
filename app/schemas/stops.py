from pydantic import BaseModel

from app.schemas.common import Point, PointBase

class StopIn(Point):
    name: str
    code: str | None = None
    osm_node_id: int | None = None
    municipality: str | None = None
    department: str | None = None
    tags: dict = {}

class StopPatch(BaseModel):
    name: str | None = None
    code: str | None = None
    lat: float | None = None
    lon: float | None = None
    z: float | None = None
    municipality: str | None = None
    department: str | None = None
    tags: dict | None = None
    is_active: bool | None = None

class StopOut(PointBase):
    id: int
    name: str
    code: str | None = None
    osm_node_id: int | None = None
    municipality: str | None = None
    department: str | None = None
    tags: dict = {}
    is_active: bool = True
    distance_m: float | None = None

class StopDetail(StopOut):
    served_by: list[dict] = []
