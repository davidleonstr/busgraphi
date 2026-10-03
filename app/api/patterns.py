import asyncpg
from fastapi import APIRouter, HTTPException, Request

from app.db.helpers import resequence
from app.dependencies import WRITE, invalidate
from app.schemas import PatternIn, PatternOut, PatternStopAdd
from app.services.patterns import load_pattern

router = APIRouter(tags=["patterns"])

@router.post("/routes/{route_id}/patterns", response_model=PatternOut, status_code=201, dependencies=WRITE)
async def create_pattern(route_id: int, body: PatternIn, request: Request):
    try:
        async with request.app.state.pool.acquire() as c, c.transaction():
            pid = await c.fetchval(
                """INSERT INTO route_patterns (route_id, direction, headsign, name, osm_relation_id)
                   VALUES ($1, $2, $3, $4, $5) RETURNING id""",
                route_id, body.direction, body.headsign, body.name, body.osm_relation_id)
            await c.executemany(
                "INSERT INTO pattern_stops (pattern_id, seq, stop_id, offset_seconds) VALUES ($1, $2, $3, $4)",
                [(pid, i, s.stop_id, s.offset_seconds) for i, s in enumerate(body.stops, 1)])
            out = await load_pattern(c, pid)
    except asyncpg.ForeignKeyViolationError:
        raise HTTPException(422, "unknown route_id or stop_id")
    invalidate(request)
    return out

@router.get("/patterns/{pattern_id}", response_model=PatternOut)
async def get_pattern(pattern_id: int, request: Request):
    async with request.app.state.pool.acquire() as c:
        return await load_pattern(c, pattern_id)

@router.delete("/patterns/{pattern_id}", status_code=204, dependencies=WRITE)
async def delete_pattern(pattern_id: int, request: Request):
    res = await request.app.state.pool.execute("DELETE FROM route_patterns WHERE id = $1", pattern_id)
    if res.endswith(" 0"):
        raise HTTPException(404, "pattern not found")
    invalidate(request)

@router.post("/patterns/{pattern_id}/stops", response_model=PatternOut, status_code=201, dependencies=WRITE)
async def add_pattern_stop(pattern_id: int, body: PatternStopAdd, request: Request):
    try:
        async with request.app.state.pool.acquire() as c, c.transaction():
            n = await c.fetchval("SELECT coalesce(max(seq), 0) FROM pattern_stops WHERE pattern_id = $1", pattern_id)
            seq = min(body.seq or n + 1, n + 1)
            await c.execute("UPDATE pattern_stops SET seq = seq + 1 WHERE pattern_id = $1 AND seq >= $2", pattern_id, seq)
            await c.execute(
                "INSERT INTO pattern_stops (pattern_id, seq, stop_id, offset_seconds) VALUES ($1, $2, $3, $4)",
                pattern_id, seq, body.stop_id, body.offset_seconds)
            out = await load_pattern(c, pattern_id)
    except asyncpg.ForeignKeyViolationError:
        raise HTTPException(404, "unknown pattern_id or stop_id")
    invalidate(request)
    return out

@router.delete("/patterns/{pattern_id}/stops/{seq}", response_model=PatternOut, dependencies=WRITE)
async def remove_pattern_stop(pattern_id: int, seq: int, request: Request):
    async with request.app.state.pool.acquire() as c, c.transaction():
        res = await c.execute("DELETE FROM pattern_stops WHERE pattern_id = $1 AND seq = $2", pattern_id, seq)
        if res.endswith(" 0"):
            raise HTTPException(404, "no stop at that position")
        await resequence(c, [pattern_id])
        out = await load_pattern(c, pattern_id)
    invalidate(request)
    return out
