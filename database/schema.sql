-- PostgreSQL 14+ with PostGIS. Coordinates are WGS84 (EPSG:4326).
-- PostGIS order is (lon, lat); the API always uses explicit lat / lon / z fields.

-- Extensions
\i extensions/postgis.sql

-- Tables
\i tables/stops.sql
\i tables/routes.sql
\i tables/route_patterns.sql
\i tables/pattern_stops.sql

-- Indexes
\i indexes/stops/stops_location_gix.sql
\i indexes/stops/stops_name_idx.sql
\i indexes/route_patterns/route_patterns_route_idx.sql

-- The indexed stop sequence: Bus 210 / pattern / Stop #1, #2, ...
\i indexes/pattern_stops/pattern_stops_stop_idx.sql