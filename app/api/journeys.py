from fastapi import APIRouter, HTTPException, Request

from app import routing
from app.dependencies import get_graph
from app.schemas import JourneyRequest, JourneyResponse
from app.services.journeys import find_candidates, point_as_path_dict

router = APIRouter(tags=["journeys"])

@router.post("/journeys/plan", response_model=JourneyResponse)
async def plan_journey(req: JourneyRequest, request: Request):
    g, pool = await get_graph(request), request.app.state.pool
    src = await find_candidates(pool, g, req.origin, req.origin_stop_id, req.max_walk_m, "origin")
    dst = await find_candidates(pool, g, req.destination, req.destination_stop_id, req.max_walk_m, "destination")
    o = routing.Options(req.transfer_walk_m, req.board_penalty_s)
    res = routing.plan(g, src, dst, point_as_path_dict(req.origin), point_as_path_dict(req.destination), o)
    if res is None:
        raise HTTPException(404, "no connection found (try a larger max_walk_m / transfer_walk_m)")
    return res
