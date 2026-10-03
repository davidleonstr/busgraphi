-- This is what lets you rebuild the route in order and drives the routing graph.
CREATE TABLE pattern_stops (
    id              BIGSERIAL PRIMARY KEY,
    pattern_id      BIGINT NOT NULL REFERENCES route_patterns(id) ON DELETE CASCADE,
    seq             INT    NOT NULL CHECK (seq > 0),
    stop_id         BIGINT NOT NULL REFERENCES stops(id) ON DELETE RESTRICT,
    offset_seconds  INT,                               -- typical time since first stop (optional)
    -- deferrable so inserting/removing a stop can shift later seq numbers in one transaction
    CONSTRAINT pattern_stops_seq_uq UNIQUE (pattern_id, seq) DEFERRABLE INITIALLY DEFERRED
);