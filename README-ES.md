# API de Buses de El Salvador

API de rutas y paradas de bus construida con FastAPI + PostGIS que incluye un planificador de viajes multitramo en memoria.

## Ejecución (Windows)
```bash
python -m venv venv
./venv/Scripts/activate
pip install -r requirements.txt
python main.py                  # o bien: uvicorn app.main:app --reload
```

Nota: `API_KEY` toma por defecto el valor original (`"TEL-AVIV"`) si la variable de entorno no está configurada; define la tuya propia en producción.