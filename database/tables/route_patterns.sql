-- One ordered itinerary of a route (outbound / inbound / variant).
CREATE TABLE route_patterns (
    id              BIGSERIAL PRIMARY KEY,
    route_id        BIGINT NOT NULL REFERENCES routes(id) ON DELETE CASCADE,
    direction       SMALLINT NOT NULL DEFAULT 0,       -- 0 = outbound, 1 = inbound
    headsign        TEXT,                              -- "toward ..."
    name            TEXT,
    osm_relation_id BIGINT UNIQUE,
    shape           geography(LineString, 4326)        -- optional road geometry
);