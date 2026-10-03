from pydantic import BaseModel, Field

from app.schemas.patterns import PatternOut

class RouteIn(BaseModel):
    code: str
    name: str | None = None
    operator: str = ""
    colour: str | None = None
    headway_min: int = Field(15, ge=1)
    avg_speed_kmh: float = Field(20, gt=0)

class RoutePatch(BaseModel):
    name: str | None = None
    colour: str | None = None
    headway_min: int | None = Field(None, ge=1)
    avg_speed_kmh: float | None = Field(None, gt=0)
    is_active: bool | None = None

class RouteOut(RouteIn):
    id: int
    is_active: bool = True
    num_patterns: int | None = None

class RouteDetail(RouteOut):
    patterns: list[PatternOut] = []
