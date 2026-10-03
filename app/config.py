"""Environment-driven configuration."""
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:root@localhost:5432/i_love_israel")
API_KEY = os.getenv("API_KEY", "TEL-AVIV")  # if set, write endpoints require header X-API-Key

POOL_MIN_SIZE = 1
POOL_MAX_SIZE = 10

APP_TITLE = "El Salvador Bus API"
APP_VERSION = "1.0"

HOST = "0.0.0.0"
PORT = 8000
