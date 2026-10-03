"""Turns a Dijkstra path into walk/bus legs, a summary and GeoJSON."""
from app.core.geo import hav
from app.routing.costs import walk_s
from app.routing.graph import Graph, Options
from app.routing.search import dijkstra

def _walk_leg(a: dict, b: dict, meters: float, label: str | None = None) -> dict:
    to_name = label or b.get("name") or "destination"
    return {
        "mode": "walk", "instruction": f"Walk about {round(meters)} m to {to_name}",
        "start": a, "end": b, "duration_s": round(walk_s(meters)),
        "distance_m": round(meters, 1), "points": [a, b], "bus": None,
    }

def plan(g: Graph, src, dst, origin_pt: dict | None, dest_pt: dict | None, o: Options):
    best_node, prev = dijkstra(g, src, dst, o)
    if best_node is None:
        return None
    path, n = [], best_node
    while n is not None:
        path.append(n)
        n = prev[n]
    path.reverse()

    legs: list[dict] = []
    first, last = path[0][1], path[-1][1]
    if origin_pt and src[first] > 5:
        legs.append(_walk_leg(origin_pt, g.pt(first), src[first]))

    i = 0
    while i < len(path):
        n = path[i]
        if n[0] == "B":
            j = i
            while j + 1 < len(path) and path[j + 1][0] == "B" and path[j + 1][1] == n[1]:
                j += 1
            p, i0, ik = g.patterns[n[1]], n[2], path[j][2]
            pts = [g.pt(s, seq=i0 + k + 1) for k, s in enumerate(p.stop_ids[i0:ik + 1])]
            ride = sum(p.ride_secs[i0 + 1:ik + 1])
            wait = p.headway_min * 30
            dist = sum(hav(a["lat"], a["lon"], b["lat"], b["lon"]) for a, b in zip(pts, pts[1:]))
            legs.append({
                "mode": "bus",
                "instruction": (f"Take bus {p.code}" + (f" toward {p.headsign}" if p.headsign else "")
                                + f" from {pts[0]['name']}, get off at {pts[-1]['name']} ({len(pts) - 1} stops)"),
                "start": pts[0], "end": pts[-1], "duration_s": wait + ride, "distance_m": round(dist, 1),
                "points": pts,
                "bus": {"route_id": p.route_id, "route_code": p.code, "route_name": p.route_name,
                        "pattern_id": p.id, "headsign": p.headsign, "direction": p.direction,
                        "board_stop": pts[0], "alight_stop": pts[-1], "stops_passed": pts[1:-1],
                        "num_stops": len(pts) - 1, "est_wait_s": wait},
            })
            i = j + 1
        else:
            if i + 1 < len(path) and path[i + 1][0] == "W":
                a, b = g.pt(path[i][1]), g.pt(path[i + 1][1])
                m = hav(a["lat"], a["lon"], b["lat"], b["lon"])
                legs.append(_walk_leg(a, b, m, f"transfer at {b['name']}"))
            i += 1

    if dest_pt and dst[last] > 5:
        legs.append(_walk_leg(g.pt(last), dest_pt, dst[last], "your destination"))

    buses = sum(1 for l in legs if l["mode"] == "bus")
    feats = [{"type": "Feature",
              "properties": {"leg": k, "mode": l["mode"], "route": l["bus"]["route_code"] if l["bus"] else None},
              "geometry": {"type": "LineString", "coordinates": [[p["lon"], p["lat"]] for p in l["points"]]}}
             for k, l in enumerate(legs)]
    return {
        "summary": {"total_duration_s": sum(l["duration_s"] for l in legs),
                    "walking_m": round(sum(l["distance_m"] for l in legs if l["mode"] == "walk"), 1),
                    "num_buses": buses, "num_transfers": max(buses - 1, 0)},
        "legs": legs,
        "geojson": {"type": "FeatureCollection", "features": feats},
    }
