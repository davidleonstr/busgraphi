# El Salvador Bus API

FastAPI + PostGIS bus stop / route API with an in-memory multi-leg journey planner.

## Run (Windows)
```bash
python -m venv venv
./venv/Scripts/activate
pip install -r requirements.txt
python main.py                  # or: uvicorn app.main:app --reload
```

Note: `API_KEY` defaults to the original value (`"TEL-AVIV"`) if the env var is unset;
set your own in production.
