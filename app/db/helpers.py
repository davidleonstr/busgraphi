"""Small SQL-building helpers shared by routers."""

def cols(a: str = "") -> str:
    """Standard stop column list (optionally table-aliased)."""
    p = f"{a}." if a else ""
    return (f"{p}id, {p}name, {p}code, ST_Y({p}location::geometry) AS lat, ST_X({p}location::geometry) AS lon, "
            f"{p}elevation_m AS z, {p}osm_node_id, {p}municipality, {p}department, {p}tags, {p}is_active")

def simple_sets(data: dict, allowed: tuple, args: list) -> list[str]:
    """Build `col = $n` fragments for the allowed keys present in data, appending values to args."""
    sets = []
    for k in allowed:
        if k in data:
            args.append(data[k])
            sets.append(f"{k} = ${len(args)}")
    return sets

async def resequence(c, pattern_ids):
    """Renumber pattern_stops.seq to be contiguous 1..n for the given patterns."""
    if pattern_ids:
        await c.execute(
            """UPDATE pattern_stops ps SET seq = r.n
               FROM (SELECT id, row_number() OVER (PARTITION BY pattern_id ORDER BY seq) AS n
                     FROM pattern_stops WHERE pattern_id = ANY($1::bigint[])) r
               WHERE ps.id = r.id AND ps.seq <> r.n""", list(pattern_ids))
