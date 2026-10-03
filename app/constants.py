"""Fixed application constants."""

# ---- geography ----
SV_BBOX = (12.9, 14.6, -90.3, -87.5)  # lat_min, lat_max, lon_min, lon_max (with margin)

# ---- routing ----
WALK_LINK_M = 300  # max stop-to-stop walking link stored in the routing graph
WALK_SPEED_MPS = 1.2
CIRCUITY = 1.3  # straight-line -> real street distance factor
DWELL_S = 20

# ---- OSM / Overpass ----
OVERPASS_URLS = ["https://overpass-api.de/api/interpreter", "https://overpass.kumi.systems/api/interpreter"]
OVERPASS_USER_AGENT = "sv-bus-api/1.0"
OVERPASS_HTTP_TIMEOUT = 400
