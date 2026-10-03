from fastapi import HTTPException

from app import routing
from app.schemas import Point

async def find_candidates(pool, g: routing.Graph, pt: Point | None, stop_id: int | None,
                          radius: int, what: str) -> dict[int, float]:
    """Return {stop_id: walking distance in m} of stops usable as journey origin/destination."""
    if stop_id is not None:
        if stop_id not in g.boardings:
            raise HTTPException(422, f"{what} stop {stop_id} does not exist or is not served by any route")
        return {stop_id: 0.0}
    rows = await pool.fetch(
        """SELECT s.id, ST_Distance(s.location, q.pt) AS d
           FROM stops s, (SELECT ST_SetSRID(ST_MakePoint($1, $2), 4326)::geography AS pt) q
           WHERE s.is_active AND ST_DWithin(s.location, q.pt, $3)
             AND EXISTS (SELECT 1 FROM pattern_stops ps WHERE ps.stop_id = s.id)
           ORDER BY d LIMIT 15""", pt.lon, pt.lat, float(radius))
    out = {r["id"]: r["d"] for r in rows if r["id"] in g.boardings}
    if not out:
        raise HTTPException(404, f"no bus stops within {radius} m of the {what}")
    return out

def point_as_path_dict(p: Point | None) -> dict | None:
    return None if p is None else {**p.model_dump(), "name": None, "stop_id": None, "seq": None}
