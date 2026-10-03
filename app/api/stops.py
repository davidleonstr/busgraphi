import asyncpg
from fastapi import APIRouter, HTTPException, Query, Request

from app.core.geo import in_sv
from app.db.helpers import cols, resequence, simple_sets
from app.dependencies import WRITE, invalidate
from app.schemas import StopDetail, StopIn, StopOut, StopPatch

router = APIRouter(tags=["stops"])

@router.post("/stops", response_model=StopOut, status_code=201, dependencies=WRITE)
async def create_stop(s: StopIn, request: Request):
    try:
        row = await request.app.state.pool.fetchrow(
            f"""INSERT INTO stops (name, code, location, elevation_m, osm_node_id, municipality, department, tags)
                VALUES ($1, $2, ST_SetSRID(ST_MakePoint($4, $3), 4326)::geography, $5, $6, $7, $8, $9)
                RETURNING {cols()}""",
            s.name, s.code, s.lat, s.lon, s.z, s.osm_node_id, s.municipality, s.department, s.tags)
    except asyncpg.UniqueViolationError:
        raise HTTPException(409, "a stop with that code or osm_node_id already exists")
    invalidate(request)
    return dict(row)

@router.get("/stops", response_model=list[StopOut])
async def list_stops(request: Request, q: str | None = None, lat: float | None = None,
                     lon: float | None = None, radius_m: int = Query(1000, le=20000),
                     limit: int = Query(100, le=1000), offset: int = 0):
    where, args, order, extra = ["is_active"], [], "id", ""
    if q:
        args.append(f"%{q}%")
        where.append(f"name ILIKE ${len(args)}")
    if lat is not None and lon is not None:
        args += [lon, lat]
        pt = f"ST_SetSRID(ST_MakePoint(${len(args) - 1}, ${len(args)}), 4326)::geography"
        args.append(float(radius_m))
        where.append(f"ST_DWithin(location, {pt}, ${len(args)})")
        order, extra = f"location <-> {pt}", f", ST_Distance(location, {pt}) AS distance_m"
    args += [limit, offset]
    rows = await request.app.state.pool.fetch(
        f"SELECT {cols()}{extra} FROM stops WHERE {' AND '.join(where)} "
        f"ORDER BY {order} LIMIT ${len(args) - 1} OFFSET ${len(args)}", *args)
    return [dict(r) for r in rows]

@router.get("/stops/{stop_id}", response_model=StopDetail)
async def get_stop(stop_id: int, request: Request):
    pool = request.app.state.pool
    row = await pool.fetchrow(f"SELECT {cols()} FROM stops WHERE id = $1", stop_id)
    if not row:
        raise HTTPException(404, "stop not found")
    served = await pool.fetch(
        """SELECT r.id AS route_id, r.code, r.name, p.id AS pattern_id, p.direction, p.headsign, ps.seq
           FROM pattern_stops ps JOIN route_patterns p ON p.id = ps.pattern_id
           JOIN routes r ON r.id = p.route_id WHERE ps.stop_id = $1 ORDER BY r.code, p.id, ps.seq""", stop_id)
    return {**dict(row), "served_by": [dict(r) for r in served]}

@router.patch("/stops/{stop_id}", response_model=StopOut, dependencies=WRITE)
async def patch_stop(stop_id: int, body: StopPatch, request: Request):
    data = body.model_dump(exclude_unset=True)
    if ("lat" in data) != ("lon" in data):
        raise HTTPException(422, "send lat and lon together")
    if "lat" in data and not in_sv(data["lat"], data["lon"]):
        raise HTTPException(422, "coordinates are outside El Salvador - check lat/lon order")
    args: list = []
    sets = simple_sets(data, ("name", "code", "municipality", "department", "tags", "is_active"), args)
    if "z" in data:
        args.append(data["z"])
        sets.append(f"elevation_m = ${len(args)}")
    if "lat" in data:
        args += [data["lon"], data["lat"]]
        sets.append(f"location = ST_SetSRID(ST_MakePoint(${len(args) - 1}, ${len(args)}), 4326)::geography")
    if not sets:
        raise HTTPException(422, "nothing to update")
    args.append(stop_id)
    row = await request.app.state.pool.fetchrow(
        f"UPDATE stops SET {', '.join(sets)}, updated_at = now() WHERE id = ${len(args)} RETURNING {cols()}", *args)
    if not row:
        raise HTTPException(404, "stop not found")
    invalidate(request)
    return dict(row)

@router.delete("/stops/{stop_id}", status_code=204, dependencies=WRITE)
async def delete_stop(stop_id: int, request: Request, force: bool = False):
    async with request.app.state.pool.acquire() as c, c.transaction():
        used = await c.fetchval("SELECT count(*) FROM pattern_stops WHERE stop_id = $1", stop_id)
        if used and not force:
            raise HTTPException(409, f"stop is used in {used} pattern position(s); use ?force=true to remove it from them")
        pats = await c.fetch("DELETE FROM pattern_stops WHERE stop_id = $1 RETURNING pattern_id", stop_id)
        await resequence(c, {r["pattern_id"] for r in pats})
        if (await c.execute("DELETE FROM stops WHERE id = $1", stop_id)).endswith(" 0"):
            raise HTTPException(404, "stop not found")
    invalidate(request)
