from fastapi import HTTPException

from app.db.helpers import cols

async def load_pattern(c, pid: int) -> dict:
    p = await c.fetchrow("SELECT * FROM route_patterns WHERE id = $1", pid)
    if not p:
        raise HTTPException(404, "pattern not found")
    rows = await c.fetch(
        f"SELECT ps.seq, ps.offset_seconds, {cols('s')} FROM pattern_stops ps "
        "JOIN stops s ON s.id = ps.stop_id WHERE ps.pattern_id = $1 ORDER BY ps.seq", pid)
    stops = [{"seq": r["seq"], "offset_seconds": r["offset_seconds"],
              "stop": {k: v for k, v in dict(r).items() if k not in ("seq", "offset_seconds")}} for r in rows]
    return {**dict(p), "stops": stops}
