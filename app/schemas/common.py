from pydantic import BaseModel, Field, model_validator

from app.core.geo import in_sv

class PointBase(BaseModel):
    lat: float = Field(ge=-90, le=90)
    lon: float = Field(ge=-180, le=180)
    z: float | None = None  # elevation (m)

class Point(PointBase):
    @model_validator(mode="after")
    def _sv(self):
        if not in_sv(self.lat, self.lon):
            raise ValueError("coordinates are outside El Salvador - check lat/lon order")
        return self
