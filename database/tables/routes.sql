-- A bus line, e.g. "210".
CREATE TABLE routes (
    id             BIGSERIAL PRIMARY KEY,
    code           TEXT NOT NULL,                      -- '210'
    name           TEXT,
    operator       TEXT NOT NULL DEFAULT '',
    colour         TEXT,
    headway_min    INT  NOT NULL DEFAULT 15 CHECK (headway_min > 0),   -- avg minutes between buses
    avg_speed_kmh  REAL NOT NULL DEFAULT 20 CHECK (avg_speed_kmh > 0),
    is_active      BOOLEAN NOT NULL DEFAULT TRUE,
    created_at     TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (code, operator)
);
