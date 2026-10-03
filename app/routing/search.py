"""Dijkstra over the state graph (see graph.py)."""
import heapq
import itertools

from app.routing.costs import walk_s
from app.routing.graph import Graph, Options

def dijkstra(g: Graph, src: dict[int, float], dst: dict[int, float], o: Options):
    inf = float("inf")
    dist, prev, done = {}, {}, set()
    heap, cnt = [], itertools.count()
    for sid, m in src.items():
        n, c = ("W", sid), walk_s(m)
        if c < dist.get(n, inf):
            dist[n], prev[n] = c, None
            heapq.heappush(heap, (c, next(cnt), n))
    best, best_node = inf, None
    while heap:
        d, _, node = heapq.heappop(heap)
        if node in done:
            continue
        done.add(node)
        if d >= best:
            break
        if node[0] == "W" and node[1] in dst:
            tot = d + walk_s(dst[node[1]])
            if tot < best:
                best, best_node = tot, node
        for nb, cost in g.neighbors(node, o):
            nd = d + cost
            if nd < dist.get(nb, inf):
                dist[nb], prev[nb] = nd, node
                heapq.heappush(heap, (nd, next(cnt), nb))
    return best_node, prev
