import asyncpg
from fastapi import APIRouter, HTTPException, Request

from app.db.helpers import simple_sets
from app.dependencies import WRITE, invalidate
from app.schemas import RouteDetail, RouteIn, RouteOut, RoutePatch
from app.services.patterns import load_pattern

router = APIRouter(tags=["routes"])

@router.get("/routes", response_model=list[RouteOut])
async def list_routes(request: Request, q: str | None = None):
    rows = await request.app.state.pool.fetch(
        """SELECT r.*, (SELECT count(*) FROM route_patterns p WHERE p.route_id = r.id) AS num_patterns
           FROM routes r WHERE ($1::text IS NULL OR r.code ILIKE $1 OR r.name ILIKE '%' || $1 || '%')
           ORDER BY r.code""", q)
    return [dict(r) for r in rows]

@router.post("/routes", response_model=RouteOut, status_code=201, dependencies=WRITE)
async def create_route(r: RouteIn, request: Request):
    try:
        row = await request.app.state.pool.fetchrow(
            """INSERT INTO routes (code, name, operator, colour, headway_min, avg_speed_kmh)
               VALUES ($1, $2, $3, $4, $5, $6) RETURNING *""",
            r.code, r.name, r.operator, r.colour, r.headway_min, r.avg_speed_kmh)
    except asyncpg.UniqueViolationError:
        raise HTTPException(409, "route code already exists for that operator")
    invalidate(request)
    return dict(row)

@router.get("/routes/{route_id}", response_model=RouteDetail)
async def get_route(route_id: int, request: Request):
    async with request.app.state.pool.acquire() as c:
        r = await c.fetchrow("SELECT * FROM routes WHERE id = $1", route_id)
        if not r:
            raise HTTPException(404, "route not found")
        pids = [x["id"] for x in await c.fetch(
            "SELECT id FROM route_patterns WHERE route_id = $1 ORDER BY direction, id", route_id)]
        return {**dict(r), "patterns": [await load_pattern(c, pid) for pid in pids]}

@router.patch("/routes/{route_id}", response_model=RouteOut, dependencies=WRITE)
async def patch_route(route_id: int, body: RoutePatch, request: Request):
    args: list = []
    sets = simple_sets(body.model_dump(exclude_unset=True),
                       ("name", "colour", "headway_min", "avg_speed_kmh", "is_active"), args)
    if not sets:
        raise HTTPException(422, "nothing to update")
    args.append(route_id)
    row = await request.app.state.pool.fetchrow(
        f"UPDATE routes SET {', '.join(sets)} WHERE id = ${len(args)} RETURNING *", *args)
    if not row:
        raise HTTPException(404, "route not found")
    invalidate(request)
    return dict(row)

@router.delete("/routes/{route_id}", status_code=204, dependencies=WRITE)
async def delete_route(route_id: int, request: Request):
    res = await request.app.state.pool.execute("DELETE FROM routes WHERE id = $1", route_id)
    if res.endswith(" 0"):
        raise HTTPException(404, "route not found")
    invalidate(request)
