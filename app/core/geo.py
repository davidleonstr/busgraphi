import math

from app.constants import SV_BBOX

def in_sv(lat: float, lon: float) -> bool:
    return SV_BBOX[0] <= lat <= SV_BBOX[1] and SV_BBOX[2] <= lon <= SV_BBOX[3]

def hav(lat1, lon1, lat2, lon2) -> float:
    """Haversine distance in metres."""
    r = 6371008.8
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp, dl = p2 - p1, math.radians(lon2 - lon1)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * r * math.asin(math.sqrt(a))
