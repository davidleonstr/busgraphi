SV_AREA = 'area["ISO3166-1"="SV"][admin_level=2]->.sv;'

Q_STOPS = f"""[out:json][timeout:300];{SV_AREA}
(node["highway"="bus_stop"](area.sv); node["public_transport"="platform"]["bus"="yes"](area.sv););
out body;"""

# relations + only their member nodes (not the whole road network)
Q_ROUTES = f"""[out:json][timeout:300];{SV_AREA}
rel["route"="bus"](area.sv)->.r; node(r.r)->.n; (.r; .n;); out body;"""
