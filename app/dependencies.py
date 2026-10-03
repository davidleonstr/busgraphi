from fastapi import Depends, Header, HTTPException, Request

from app import routing
from app.config import API_KEY

def require_key(x_api_key: str | None = Header(None)):
    if API_KEY and x_api_key != API_KEY:
        raise HTTPException(401, "invalid or missing X-API-Key")

WRITE = [Depends(require_key)]

def invalidate(request: Request):
    request.app.state.graph = None  # routing graph is rebuilt lazily on next plan request

async def get_graph(request: Request) -> routing.Graph:
    st = request.app.state
    if st.graph is None:
        async with st.lock:
            if st.graph is None:
                st.graph = await routing.load_graph(st.pool)
    return st.graph
