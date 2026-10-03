from fastapi import APIRouter, HTTPException, Request

from app import osm
from app.dependencies import WRITE, invalidate

router = APIRouter(prefix="/osm/import", tags=["osm"])

@router.post("/stops", dependencies=WRITE)
async def osm_import_stops(request: Request):
    try:
        out = await osm.import_stops(request.app.state.pool)
    except RuntimeError as e:
        raise HTTPException(502, str(e))
    invalidate(request)
    return out

@router.post("/routes", dependencies=WRITE)
async def osm_import_routes(request: Request):
    try:
        out = await osm.import_routes(request.app.state.pool)
    except RuntimeError as e:
        raise HTTPException(502, str(e))
    invalidate(request)
    return out
