from collections import defaultdict

from app.osm.client import overpass
from app.osm.queries import Q_ROUTES, Q_STOPS

async def _upsert_nodes(c, nodes: list[dict]) -> int:
    rows = []
    for n in nodes:
        t = n.get("tags", {})
        name = t.get("name") or t.get("ref") or f"OSM stop {n['id']}"
        rows.append((name, n["id"], n["lat"], n["lon"], t))
    await c.executemany(
        """INSERT INTO stops (name, osm_node_id, location, tags)
           VALUES ($1, $2, ST_SetSRID(ST_MakePoint($4, $3), 4326)::geography, $5)
           ON CONFLICT (osm_node_id) DO UPDATE
             SET name = EXCLUDED.name, location = EXCLUDED.location,
                 tags = EXCLUDED.tags, updated_at = now()""", rows)
    return len(rows)

async def import_stops(pool) -> dict:
    els = await overpass(Q_STOPS)
    nodes = [e for e in els if e["type"] == "node" and "lat" in e]
    async with pool.acquire() as c, c.transaction():
        n = await _upsert_nodes(c, nodes)
    return {"stops_upserted": n}

async def import_routes(pool) -> dict:
    els = await overpass(Q_ROUTES)
    nodes = {e["id"]: e for e in els if e["type"] == "node" and "lat" in e}
    rels = [e for e in els if e["type"] == "relation"]
    done = skipped = 0
    async with pool.acquire() as c, c.transaction():
        await _upsert_nodes(c, list(nodes.values()))
        idmap = {r["osm_node_id"]: r["id"] for r in await c.fetch(
            "SELECT id, osm_node_id FROM stops WHERE osm_node_id = ANY($1::bigint[])", list(nodes))}
        seen = defaultdict(int)
        for rel in rels:
            t = rel.get("tags", {})
            members = [m for m in rel.get("members", []) if m["type"] == "node"]
            chosen = [m for m in members if m["role"].startswith("stop")] or \
                     [m for m in members if m["role"].startswith("platform")]
            ids = []
            for m in chosen:
                sid = idmap.get(m["ref"])
                if sid and (not ids or ids[-1] != sid):
                    ids.append(sid)
            if len(ids) < 2:
                skipped += 1
                continue
            code = t.get("ref") or t.get("name") or f"rel{rel['id']}"
            route_id = await c.fetchval(
                """INSERT INTO routes (code, name, operator) VALUES ($1, $2, $3)
                   ON CONFLICT (code, operator) DO UPDATE SET name = coalesce(routes.name, EXCLUDED.name)
                   RETURNING id""", code, t.get("name"), t.get("operator", ""))
            direction = seen[route_id] % 2  # heuristic: 1st relation = outbound, 2nd = inbound
            seen[route_id] += 1
            pid = await c.fetchval(
                """INSERT INTO route_patterns (route_id, direction, headsign, name, osm_relation_id)
                   VALUES ($1, $2, $3, $4, $5)
                   ON CONFLICT (osm_relation_id) DO UPDATE
                     SET route_id = EXCLUDED.route_id, headsign = EXCLUDED.headsign, name = EXCLUDED.name
                   RETURNING id""", route_id, direction, t.get("to"), t.get("name"), rel["id"])
            await c.execute("DELETE FROM pattern_stops WHERE pattern_id = $1", pid)
            await c.executemany("INSERT INTO pattern_stops (pattern_id, seq, stop_id) VALUES ($1, $2, $3)",
                                [(pid, i, s) for i, s in enumerate(ids, 1)])
            done += 1
    return {"patterns_imported": done, "relations_skipped": skipped}
