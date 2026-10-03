-- A physical bus stop. "z" = elevation in metres (optional).
CREATE TABLE stops (
    id            BIGSERIAL PRIMARY KEY,
    name          TEXT        NOT NULL,
    code          TEXT UNIQUE,                         -- your own stop code, e.g. 'PA-01'
    location      geography(Point, 4326) NOT NULL,
    elevation_m   REAL,
    osm_node_id   BIGINT UNIQUE,                       -- link to OpenStreetMap node
    municipality  TEXT,
    department    TEXT,
    tags          JSONB       NOT NULL DEFAULT '{}',   -- raw OSM tags / extras
    is_active     BOOLEAN     NOT NULL DEFAULT TRUE,
    created_at    TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at    TIMESTAMPTZ NOT NULL DEFAULT now()
);