"""Routing graph model and loader.

Nodes
  ("W", stop_id)            - standing at a stop on foot (just arrived / about to board)
  ("B", pattern_id, idx)    - aboard a bus of that pattern, currently at its idx-th stop
Edges
  W -> B   board   cost = headway/2 (expected wait) + board_penalty
  B -> B   ride    cost = time to next stop (offset_seconds if known, else distance / speed)
  B -> W   alight  cost = 0
  W -> W   walk    cost = distance * circuity / walking speed (<= transfer_walk_m)
"""
from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field

from app.constants import CIRCUITY, DWELL_S, WALK_LINK_M
from app.routing.costs import walk_s

PATTERN_SQL = """
SELECT p.id AS pattern_id, r.id AS route_id, r.code, r.name AS route_name, r.headway_min,
       r.avg_speed_kmh, p.headsign, p.direction, ps.stop_id, ps.offset_seconds,
       ST_Distance(s.location, LAG(s.location) OVER w) AS dist_prev
FROM pattern_stops ps
JOIN route_patterns p ON p.id = ps.pattern_id
JOIN routes r ON r.id = p.route_id
JOIN stops  s ON s.id = ps.stop_id
WHERE r.is_active AND s.is_active
WINDOW w AS (PARTITION BY ps.pattern_id ORDER BY ps.seq)
ORDER BY ps.pattern_id, ps.seq
"""
WALK_SQL = """
SELECT a.id AS a, b.id AS b, ST_Distance(a.location, b.location) AS d
FROM stops a JOIN stops b ON a.id <> b.id AND ST_DWithin(a.location, b.location, $1)
WHERE a.is_active AND b.is_active
"""

@dataclass
class Pattern:
    id: int
    route_id: int
    code: str
    route_name: str | None
    headway_min: int
    headsign: str | None
    direction: int
    stop_ids: list[int] = field(default_factory=list)
    ride_secs: list[int] = field(default_factory=list)  # ride_secs[i] = time from stop i-1 to i
    _prev_offset: int | None = None

@dataclass
class Options:
    transfer_walk_m: int = 300
    board_penalty_s: int = 120

class Graph:
    def __init__(self):
        self.stops: dict[int, dict] = {}
        self.patterns: dict[int, Pattern] = {}
        self.boardings: dict[int, list[tuple[int, int]]] = defaultdict(list)
        self.walks: dict[int, list[tuple[int, float]]] = defaultdict(list)

    def pt(self, stop_id: int, seq: int | None = None) -> dict:
        s = self.stops[stop_id]
        return {"lat": s["lat"], "lon": s["lon"], "z": s["z"], "name": s["name"], "stop_id": stop_id, "seq": seq}

    def neighbors(self, node, o: Options):
        if node[0] == "W":
            sid = node[1]
            for pid, idx in self.boardings.get(sid, ()):
                p = self.patterns[pid]
                if idx < len(p.stop_ids) - 1:  # no point boarding at the terminus
                    yield ("B", pid, idx), p.headway_min * 30 + o.board_penalty_s
            for t, dm in self.walks.get(sid, ()):
                if dm <= o.transfer_walk_m:
                    yield ("W", t), walk_s(dm)
        else:
            _, pid, idx = node
            p = self.patterns[pid]
            yield ("W", p.stop_ids[idx]), 0.0
            if idx + 1 < len(p.stop_ids):
                yield ("B", pid, idx + 1), p.ride_secs[idx + 1]

async def load_graph(pool) -> Graph:
    g = Graph()
    async with pool.acquire() as c:
        for r in await c.fetch(
            "SELECT id, name, ST_Y(location::geometry) AS lat, ST_X(location::geometry) AS lon, "
            "elevation_m AS z FROM stops WHERE is_active"
        ):
            g.stops[r["id"]] = dict(r)
        for r in await c.fetch(PATTERN_SQL):
            p = g.patterns.get(r["pattern_id"])
            if p is None:
                p = g.patterns[r["pattern_id"]] = Pattern(
                    r["pattern_id"], r["route_id"], r["code"], r["route_name"],
                    r["headway_min"], r["headsign"], r["direction"])
            off = r["offset_seconds"]
            if not p.stop_ids:
                secs = 0
            elif off is not None and p._prev_offset is not None and off > p._prev_offset:
                secs = off - p._prev_offset
            else:
                speed = max(r["avg_speed_kmh"], 5) / 3.6
                secs = int((r["dist_prev"] or 0) * CIRCUITY / speed) + DWELL_S
            p._prev_offset = off
            g.boardings[r["stop_id"]].append((p.id, len(p.stop_ids)))
            p.stop_ids.append(r["stop_id"])
            p.ride_secs.append(secs)
        for r in await c.fetch(WALK_SQL, float(WALK_LINK_M)):
            g.walks[r["a"]].append((r["b"], r["d"]))
    return g
