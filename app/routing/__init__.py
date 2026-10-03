"""In-memory multi-leg transit router (Dijkstra over a time-expanded-free state graph).

Origin/destination coordinates connect to every nearby stop with a walking cost, so the
"best" boarding stop is found by the search itself, not guessed as "the nearest one".
"""
from app.routing.graph import Graph, Options, Pattern, load_graph
from app.routing.planner import plan

__all__ = ["Graph", "Options", "Pattern", "load_graph", "plan"]
