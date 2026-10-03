import httpx

from app.constants import OVERPASS_HTTP_TIMEOUT, OVERPASS_URLS, OVERPASS_USER_AGENT

async def overpass(query: str) -> list[dict]:
    last = None
    async with httpx.AsyncClient(timeout=OVERPASS_HTTP_TIMEOUT, headers={"User-Agent": OVERPASS_USER_AGENT}) as cl:
        for url in OVERPASS_URLS:
            try:
                r = await cl.post(url, data={"data": query})
                r.raise_for_status()
                return r.json()["elements"]
            except Exception as e:  # try the next mirror
                last = e
    raise RuntimeError(f"Overpass request failed: {last}")
