from fastapi import APIRouter

from app.api import journeys, osm, patterns, routes, stops

api_router = APIRouter()
for _m in (stops, routes, patterns, journeys, osm):
    api_router.include_router(_m.router)
