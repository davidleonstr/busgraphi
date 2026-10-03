-- The file was not split because it needs to be easily manageable by LLM agents.
-- =====================================================================
-- El Salvador Bus API - Test-oriented dataset
-- 100% ASCII
-- =====================================================================

BEGIN;

-- ---------------------------------------------------------------------
-- 0. Reset
-- ---------------------------------------------------------------------
TRUNCATE pattern_stops, route_patterns, routes, stops RESTART IDENTITY CASCADE;

-- ---------------------------------------------------------------------
-- 1. STOPS
-- ---------------------------------------------------------------------
INSERT INTO stops (name, code, location, elevation_m, osm_node_id, municipality, department, tags) VALUES
  -- San Salvador
  ('Terminal de Occidente (San Salvador)', 'SS-TOCC-01', ST_SetSRID(ST_MakePoint(-89.2500, 13.6900),4326)::geography, 680, NULL, 'San Salvador', 'San Salvador', '{"type":"terminal"}'::jsonb),
  ('Terminal de Oriente (San Salvador)',   'SS-TORI-01', ST_SetSRID(ST_MakePoint(-89.2182, 13.6929),4326)::geography, 660, NULL, 'San Salvador', 'San Salvador', '{"type":"terminal"}'::jsonb),
  ('Terminal del Sur (San Salvador)',      'SS-TSUR-01', ST_SetSRID(ST_MakePoint(-89.2100, 13.6700),4326)::geography, 650, NULL, 'San Salvador', 'San Salvador', '{"type":"terminal"}'::jsonb),
  ('Metrocentro',                          'SS-MC-01',   ST_SetSRID(ST_MakePoint(-89.2244, 13.7013),4326)::geography, 670, NULL, 'San Salvador', 'San Salvador', '{"type":"mall"}'::jsonb),
  ('Centro Historico (Plaza Morazan)',     'SS-CH-01',   ST_SetSRID(ST_MakePoint(-89.1911, 13.6929),4326)::geography, 655, NULL, 'San Salvador', 'San Salvador', '{"type":"historic"}'::jsonb),
  ('Universidad de El Salvador (UES)',     'SS-UES-01',  ST_SetSRID(ST_MakePoint(-89.2036, 13.7186),4326)::geography, 710, NULL, 'San Salvador', 'San Salvador', '{"type":"university"}'::jsonb),
  ('Hospital Rosales',                     'SS-HR-01',   ST_SetSRID(ST_MakePoint(-89.2190, 13.6919),4326)::geography, 665, NULL, 'San Salvador', 'San Salvador', '{"type":"hospital"}'::jsonb),
  ('Redondel Masferrer',                   'SS-RM-01',   ST_SetSRID(ST_MakePoint(-89.2477, 13.7010),4326)::geography, 705, NULL, 'San Salvador', 'San Salvador', '{"type":"landmark"}'::jsonb),
  ('El Boqueron',                          'SS-BOQ-01',  ST_SetSRID(ST_MakePoint(-89.2900, 13.7300),4326)::geography, 1800, NULL, 'San Salvador', 'San Salvador', '{"type":"volcano"}'::jsonb),

  -- AMSS
  ('Terminal de Buses de Soyapango', 'SO-TERM-01', ST_SetSRID(ST_MakePoint(-89.1400, 13.6175),4326)::geography, 620, NULL, 'Soyapango', 'San Salvador', '{"type":"terminal"}'::jsonb),
  ('Plaza Mundo Soyapango',          'SO-PM-01',   ST_SetSRID(ST_MakePoint(-89.1500, 13.6300),4326)::geography, 630, NULL, 'Soyapango', 'San Salvador', '{"type":"mall"}'::jsonb),
  ('Universidad Don Bosco (UDB)',    'SO-UDB-01',  ST_SetSRID(ST_MakePoint(-89.1450, 13.6500),4326)::geography, 610, NULL, 'Soyapango', 'San Salvador', '{"type":"university"}'::jsonb),
  ('Apopa Centro',                   'AP-CN-01',   ST_SetSRID(ST_MakePoint(-89.1800, 13.8000),4326)::geography, 480, NULL, 'Apopa', 'San Salvador', '{"type":"city"}'::jsonb),
  ('Mejicanos Centro',               'ME-CN-01',   ST_SetSRID(ST_MakePoint(-89.2130, 13.7400),4326)::geography, 660, NULL, 'Mejicanos', 'San Salvador', '{"type":"city"}'::jsonb),
  ('Colonia Zacamil',                'ME-ZAC-01',  ST_SetSRID(ST_MakePoint(-89.2200, 13.7450),4326)::geography, 665, NULL, 'Mejicanos', 'San Salvador', '{"type":"neighborhood"}'::jsonb),
  ('Ciudad Delgado',                 'CD-CN-01',   ST_SetSRID(ST_MakePoint(-89.1700, 13.7200),4326)::geography, 640, NULL, 'Ciudad Delgado', 'San Salvador', '{"type":"city"}'::jsonb),
  ('Ilopango Centro',                'IL-CN-01',   ST_SetSRID(ST_MakePoint(-89.1100, 13.6950),4326)::geography, 600, NULL, 'Ilopango', 'San Salvador', '{"type":"city"}'::jsonb),

  -- La Libertad
  ('Terminal de Buses de Santa Tecla', 'ST-TERM-01', ST_SetSRID(ST_MakePoint(-89.2797, 13.6769),4326)::geography, 930, NULL, 'Santa Tecla', 'La Libertad', '{"type":"terminal"}'::jsonb),
  ('Plaza Merliot',                    'ST-PM-01',   ST_SetSRID(ST_MakePoint(-89.2900, 13.6780),4326)::geography, 900, NULL, 'Santa Tecla', 'La Libertad', '{"type":"mall"}'::jsonb),
  ('Basilica de Guadalupe',            'AC-BG-01',   ST_SetSRID(ST_MakePoint(-89.2400, 13.6700),4326)::geography, 800, NULL, 'Antiguo Cuscatlan', 'La Libertad', '{"type":"church"}'::jsonb),
  ('Puerto de La Libertad',            'LL-PTO-01',  ST_SetSRID(ST_MakePoint(-89.3225, 13.4886),4326)::geography, 15,  NULL, 'La Libertad', 'La Libertad', '{"type":"port"}'::jsonb),
  ('Playa El Tunco',                   'LL-TUN-01',  ST_SetSRID(ST_MakePoint(-89.3900, 13.4950),4326)::geography, 5,   NULL, 'Tamanique', 'La Libertad', '{"type":"beach"}'::jsonb),
  ('Playa El Sunzal',                  'LL-SUN-01',  ST_SetSRID(ST_MakePoint(-89.4000, 13.4930),4326)::geography, 8,   NULL, 'Tamanique', 'La Libertad', '{"type":"beach"}'::jsonb),
  ('Zaragoza Centro',                  'ZA-CN-01',   ST_SetSRID(ST_MakePoint(-89.2800, 13.5800),4326)::geography, 400, NULL, 'Zaragoza', 'La Libertad', '{"type":"city"}'::jsonb),

  -- Santa Ana
  ('Terminal de Buses de Santa Ana (TUDO)', 'SA-TERM-01', ST_SetSRID(ST_MakePoint(-89.5610, 13.9880),4326)::geography, 640, NULL, 'Santa Ana', 'Santa Ana', '{"type":"terminal"}'::jsonb),
  ('Catedral de Santa Ana',                 'SA-CAT-01',  ST_SetSRID(ST_MakePoint(-89.5560, 13.9940),4326)::geography, 650, NULL, 'Santa Ana', 'Santa Ana', '{"type":"church"}'::jsonb),
  ('Chalchuapa Centro',                     'CH-CN-01',   ST_SetSRID(ST_MakePoint(-89.6800, 13.9800),4326)::geography, 720, NULL, 'Chalchuapa', 'Santa Ana', '{"type":"city"}'::jsonb),
  ('Metapan Centro',                        'MT-CN-01',   ST_SetSRID(ST_MakePoint(-89.4500, 14.3300),4326)::geography, 470, NULL, 'Metapan', 'Santa Ana', '{"type":"city"}'::jsonb),

  -- Ahuachapan
  ('Terminal de Buses de Ahuachapan', 'AH-TERM-01', ST_SetSRID(ST_MakePoint(-89.8390, 13.9276),4326)::geography, 800, NULL, 'Ahuachapan', 'Ahuachapan', '{"type":"terminal"}'::jsonb),
  ('Atiquizaya Centro',               'AT-CN-01',   ST_SetSRID(ST_MakePoint(-89.7600, 13.9700),4326)::geography, 780, NULL, 'Atiquizaya', 'Ahuachapan', '{"type":"city"}'::jsonb),
  ('Apaneca Centro',                  'AP-AP-01',   ST_SetSRID(ST_MakePoint(-89.8000, 13.8600),4326)::geography, 1200,NULL, 'Apaneca', 'Ahuachapan', '{"type":"city"}'::jsonb),
  ('Concepcion de Ataco',             'AT-CO-01',   ST_SetSRID(ST_MakePoint(-89.8500, 13.8700),4326)::geography, 1100,NULL, 'Concepcion de Ataco', 'Ahuachapan', '{"type":"city"}'::jsonb),

  -- Sonsonate
  ('Nueva Terminal de Sonsonate', 'SN-TERM-01', ST_SetSRID(ST_MakePoint(-89.7242, 13.7189),4326)::geography, 220, NULL, 'Sonsonate', 'Sonsonate', '{"type":"terminal"}'::jsonb),
  ('Izalco Centro',               'IZ-CN-01',   ST_SetSRID(ST_MakePoint(-89.6800, 13.7400),4326)::geography, 550, NULL, 'Izalco', 'Sonsonate', '{"type":"city"}'::jsonb),
  ('Acajutla Puerto',             'AC-PTO-01',  ST_SetSRID(ST_MakePoint(-89.8300, 13.5900),4326)::geography, 10,  NULL, 'Acajutla', 'Sonsonate', '{"type":"port"}'::jsonb),
  ('Playa Los Cobanos',           'LL-COB-01',  ST_SetSRID(ST_MakePoint(-89.8100, 13.5200),4326)::geography, 5,   NULL, 'Acajutla', 'Sonsonate', '{"type":"beach"}'::jsonb),

  -- San Miguel / Oriente
  ('Terminal de Buses de San Miguel', 'SM-TERM-01', ST_SetSRID(ST_MakePoint(-88.1770, 13.4790),4326)::geography, 105, NULL, 'San Miguel', 'San Miguel', '{"type":"terminal"}'::jsonb),
  ('Catedral de San Miguel',          'SM-CAT-01',  ST_SetSRID(ST_MakePoint(-88.1833, 13.4833),4326)::geography, 110, NULL, 'San Miguel', 'San Miguel', '{"type":"church"}'::jsonb),
  ('Usulutan Centro',                 'US-CN-01',   ST_SetSRID(ST_MakePoint(-88.4600, 13.3500),4326)::geography, 90,  NULL, 'Usulutan', 'Usulutan', '{"type":"city"}'::jsonb),
  ('San Vicente Centro',              'SV-CN-01',   ST_SetSRID(ST_MakePoint(-88.7800, 13.6400),4326)::geography, 400, NULL, 'San Vicente', 'San Vicente', '{"type":"city"}'::jsonb),
  ('Zacatecoluca Centro',             'ZA-CN-01',   ST_SetSRID(ST_MakePoint(-88.8700, 13.5100),4326)::geography, 210, NULL, 'Zacatecoluca', 'La Paz', '{"type":"city"}'::jsonb),
  ('La Union Centro',                 'LU-CN-01',   ST_SetSRID(ST_MakePoint(-87.8400, 13.3400),4326)::geography, 15,  NULL, 'La Union', 'La Union', '{"type":"city"}'::jsonb),

  -- Chalatenango / Norte
  ('Terminal de Buses de Chalatenango', 'CA-TERM-01', ST_SetSRID(ST_MakePoint(-88.9300, 14.0400),4326)::geography, 400, NULL, 'Chalatenango', 'Chalatenango', '{"type":"terminal"}'::jsonb),
  ('La Palma Centro',                   'LP-CN-01',   ST_SetSRID(ST_MakePoint(-89.1200, 14.3200),4326)::geography, 1000,NULL, 'La Palma', 'Chalatenango', '{"type":"city"}'::jsonb),
  ('San Ignacio Centro',                'SI-CN-01',   ST_SetSRID(ST_MakePoint(-89.1800, 14.2500),4326)::geography, 900, NULL, 'San Ignacio', 'Chalatenango', '{"type":"city"}'::jsonb),
  ('Cojutepeque Centro',                'CO-CN-01',   ST_SetSRID(ST_MakePoint(-88.9300, 13.7200),4326)::geography, 700, NULL, 'Cojutepeque', 'Cuscatlan', '{"type":"city"}'::jsonb),
  ('Suchitoto Centro',                  'SU-CN-01',   ST_SetSRID(ST_MakePoint(-89.0300, 13.9400),4326)::geography, 500, NULL, 'Suchitoto', 'Cuscatlan', '{"type":"city"}'::jsonb),

  -- Sur / Aeropuerto
  ('Aeropuerto Monsenor Romero', 'AI-APT-01', ST_SetSRID(ST_MakePoint(-89.0600, 13.4400),4326)::geography, 30, NULL, 'San Luis Talpa', 'La Paz', '{"type":"airport"}'::jsonb)
ON CONFLICT (code) DO NOTHING;

-- ---------------------------------------------------------------------
-- 2. ROUTES
-- ---------------------------------------------------------------------
INSERT INTO routes (code, name, operator, colour, headway_min, avg_speed_kmh) VALUES
  ('202',    'Ahuachapan - San Salvador (via CA-8)',          'ACOP', '#8B4513', 20, 45),
  ('201',    'Santa Ana - San Salvador (TUDO)',               'TUDO', '#7B2D8B', 25, 50),
  ('205',    'Sonsonate - San Salvador (Terminal Occidente)', 'ACOP', '#00A0B0', 20, 40),
  ('302',    'San Miguel - San Salvador',                     'ACOP', '#D6336C', 45, 50),
  ('125',    'Chalatenango - San Salvador',                   'ACOP', '#8B0000', 30, 45),
  ('119',    'San Salvador - San Ignacio (via El Pital)',     'ACOP', '#2E8B57', 60, 35),
  ('509',    'San Ignacio - Rio Chiquito',                    'ACOP', '#556B2F', 90, 25),
  ('44',     'Zacamil - Antiguo Cuscatlan (via UES)',         'ACOP', '#009639', 10, 22),
  ('29',     'Ilopango - Centro Historico San Salvador',      'ACOP', '#F5A623', 12, 20),
  ('7',      'Soyapango - San Salvador',                      'ACOP', '#FF4500',  8, 18),
  ('101',    'Santa Tecla - San Salvador',                    'ACOP', '#32CD32',  8, 20),
  ('102',    'Puerto La Libertad - San Salvador',             'ACOP', '#1E90FF', 15, 25),
  ('102-A',  'La Ceiba - El Tunco / El Sunzal',               'ACOP', '#00BFFF', 30, 30),
  ('103',    'La Ceiba - El Boqueron',                        'ACOP', '#8FBC8F', 40, 20),
  ('218',    'Ahuachapan - Santa Ana (via Chalchuapa)',       'ACOP', '#A0522D', 15, 40),
  ('249',    'Sonsonate - Ruta de las Flores',                'ACOP', '#FF69B4', 30, 35),
  ('257',    'Sonsonate - Playa Los Cobanos',                 'ACOP', '#87CEEB', 30, 30),
  ('19',     'San Salvador - UDB Ciudadela Don Bosco',        'ACOP', '#191970', 15, 20),
  ('140x7',  'San Salvador - UDB (Carretera de Oro)',         'ACOP', '#000080', 20, 25),
  ('TEST-ALL','Smoke-test line (todas las paradas)',          'test', NULL,      10, 30)
ON CONFLICT (code, operator) DO UPDATE
  SET name = EXCLUDED.name, colour = EXCLUDED.colour,
      headway_min = EXCLUDED.headway_min, avg_speed_kmh = EXCLUDED.avg_speed_kmh,
      is_active = TRUE;

-- ---------------------------------------------------------------------
-- 3. PATTERNS
-- ---------------------------------------------------------------------

-- 3.1 TEST-ALL
INSERT INTO route_patterns (route_id, direction, headsign, name)
SELECT id, 0, 'loop', 'All-stops smoke test' FROM routes WHERE code = 'TEST-ALL';

INSERT INTO pattern_stops (pattern_id, seq, stop_id)
SELECT p.id, row_number() OVER (ORDER BY s.id), s.id
FROM route_patterns p
JOIN routes r ON r.id = p.route_id AND r.code = 'TEST-ALL' AND p.direction = 0
CROSS JOIN stops s WHERE s.is_active;

-- 3.2 Real routes
DO $$
DECLARE
    pats CONSTANT jsonb := '[
        {"code":"202","dir":0,"headsign":"San Salvador","name":"Ahuachapan -> San Salvador","stops":["AH-TERM-01","AT-CN-01","CH-CN-01","SA-TERM-01","SS-TOCC-01"]},
        {"code":"202","dir":1,"headsign":"Ahuachapan","name":"San Salvador -> Ahuachapan","stops":["SS-TOCC-01","SA-TERM-01","CH-CN-01","AT-CN-01","AH-TERM-01"]},

        {"code":"218","dir":0,"headsign":"Santa Ana","name":"Ahuachapan -> Santa Ana","stops":["AH-TERM-01","AT-CN-01","CH-CN-01","SA-TERM-01"]},
        {"code":"218","dir":1,"headsign":"Ahuachapan","name":"Santa Ana -> Ahuachapan","stops":["SA-TERM-01","CH-CN-01","AT-CN-01","AH-TERM-01"]},

        {"code":"201","dir":0,"headsign":"San Salvador","name":"Santa Ana -> San Salvador","stops":["SA-TERM-01","SS-TOCC-01"]},
        {"code":"201","dir":1,"headsign":"Santa Ana","name":"San Salvador -> Santa Ana","stops":["SS-TOCC-01","SA-TERM-01"]},

        {"code":"205","dir":0,"headsign":"San Salvador","name":"Sonsonate -> San Salvador","stops":["SN-TERM-01","SS-TOCC-01"]},
        {"code":"205","dir":1,"headsign":"Sonsonate","name":"San Salvador -> Sonsonate","stops":["SS-TOCC-01","SN-TERM-01"]},

        {"code":"302","dir":0,"headsign":"San Salvador","name":"San Miguel -> San Salvador","stops":["SM-TERM-01","US-CN-01","SV-CN-01","ZA-CN-01","SS-TORI-01"]},

        {"code":"125","dir":0,"headsign":"San Salvador","name":"Chalatenango -> San Salvador","stops":["CA-TERM-01","SS-TORI-01"]},
        {"code":"125","dir":1,"headsign":"Chalatenango","name":"San Salvador -> Chalatenango","stops":["SS-TORI-01","CA-TERM-01"]},

        {"code":"44","dir":0,"headsign":"Antiguo Cuscatlan","name":"Zacamil -> Antiguo Cuscatlan","stops":["ME-ZAC-01","SS-UES-01","SS-MC-01","AC-BG-01"]},
        {"code":"44","dir":1,"headsign":"Zacamil","name":"Antiguo Cuscatlan -> Zacamil","stops":["AC-BG-01","SS-MC-01","SS-UES-01","ME-ZAC-01"]},

        {"code":"29","dir":0,"headsign":"Centro Historico","name":"Ilopango -> Centro Historico","stops":["IL-CN-01","SS-CH-01"]},
        {"code":"29","dir":1,"headsign":"Ilopango","name":"Centro Historico -> Ilopango","stops":["SS-CH-01","IL-CN-01"]},

        {"code":"7","dir":0,"headsign":"San Salvador","name":"Soyapango -> San Salvador","stops":["SO-TERM-01","SS-CH-01"]},
        {"code":"7","dir":1,"headsign":"Soyapango","name":"San Salvador -> Soyapango","stops":["SS-CH-01","SO-TERM-01"]},

        {"code":"101","dir":0,"headsign":"San Salvador","name":"Santa Tecla -> San Salvador","stops":["ST-TERM-01","SS-TOCC-01"]},
        {"code":"101","dir":1,"headsign":"Santa Tecla","name":"San Salvador -> Santa Tecla","stops":["SS-TOCC-01","ST-TERM-01"]},

        {"code":"102","dir":0,"headsign":"San Salvador","name":"Puerto La Libertad -> San Salvador","stops":["LL-PTO-01","ZA-CN-01","ST-TERM-01","SS-TOCC-01"]},
        {"code":"102","dir":1,"headsign":"Puerto La Libertad","name":"San Salvador -> Puerto La Libertad","stops":["SS-TOCC-01","ST-TERM-01","ZA-CN-01","LL-PTO-01"]},

        {"code":"102-A","dir":0,"headsign":"El Sunzal","name":"La Ceiba -> El Tunco y El Sunzal","stops":["LL-TUN-01","LL-SUN-01"]},
        {"code":"102-A","dir":1,"headsign":"La Ceiba","name":"El Sunzal -> El Tunco y La Ceiba","stops":["LL-SUN-01","LL-TUN-01"]},

        {"code":"103","dir":0,"headsign":"El Boqueron","name":"La Ceiba -> El Boqueron","stops":["SS-BOQ-01"]},

        {"code":"249","dir":0,"headsign":"Ahuachapan","name":"Sonsonate -> Ahuachapan (Ruta Flores)","stops":["SN-TERM-01","AP-AP-01","AT-CO-01","AH-TERM-01"]},
        {"code":"249","dir":1,"headsign":"Sonsonate","name":"Ahuachapan -> Sonsonate (Ruta Flores)","stops":["AH-TERM-01","AT-CO-01","AP-AP-01","SN-TERM-01"]},

        {"code":"257","dir":0,"headsign":"Los Cobanos","name":"Sonsonate -> Los Cobanos","stops":["SN-TERM-01","LL-COB-01"]},
        {"code":"257","dir":1,"headsign":"Sonsonate","name":"Los Cobanos -> Sonsonate","stops":["LL-COB-01","SN-TERM-01"]},

        {"code":"19","dir":0,"headsign":"UDB","name":"San Salvador -> UDB","stops":["SS-CH-01","SO-UDB-01"]},

        {"code":"140x7","dir":0,"headsign":"UDB","name":"San Salvador -> UDB (Carretera Oro)","stops":["SS-CH-01","AP-CN-01","SO-UDB-01"]},

        {"code":"119","dir":0,"headsign":"San Ignacio","name":"San Salvador -> San Ignacio","stops":["SS-TORI-01","CA-TERM-01","SI-CN-01"]},
        {"code":"119","dir":1,"headsign":"San Salvador","name":"San Ignacio -> San Salvador","stops":["SI-CN-01","CA-TERM-01","SS-TORI-01"]},

        {"code":"509","dir":0,"headsign":"Rio Chiquito","name":"San Ignacio -> Rio Chiquito","stops":["SI-CN-01","LP-CN-01"]}
    ]'::jsonb;
    pat jsonb;
    rid bigint;
    pid bigint;
    i   int;
BEGIN
    FOR pat IN SELECT jsonb_array_elements(pats) LOOP
        SELECT id INTO rid FROM routes WHERE code = pat->>'code';
        IF rid IS NULL THEN
            RAISE NOTICE 'route % missing, skipping', pat->>'code';
            CONTINUE;
        END IF;

        INSERT INTO route_patterns (route_id, direction, headsign, name)
        VALUES (rid, (pat->>'dir')::int, pat->>'headsign', pat->>'name')
        RETURNING id INTO pid;

        FOR i IN 0 .. jsonb_array_length(pat->'stops') - 1 LOOP
            INSERT INTO pattern_stops (pattern_id, seq, stop_id)
            VALUES (pid, i + 1, (SELECT id FROM stops WHERE code = pat->'stops'->>i));
        END LOOP;
    END LOOP;
END $$;

COMMIT;