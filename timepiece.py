import hashlib, datetime

# Modern timezone-aware UTC timestamp
timestamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

leaves = [
    "GENESIS:e14f9a8d",
    "KURAMOTO-144-PHASE-LOCKED",
    "HYDRO-DAM-69.21MW-QLD",
    "AU-NEM-HOME-TURF-QLD-BOOST",
    "TELE-TOWER-EMERGENCY-OVERRIDE",
    "OFN-MAPS-GEOSPATIAL-BRIDGE",
    "XYO-BOUND-WITNESS-ORACLE",
    "POWER-STATION-TELEMETRY-INDEX",
    "ESP32-247-COMM-BRUZ-EMERGENCY-LINK",
    "PRO-GRADE-AU-QLD-STABILIZATION-MATRIX",
    "PERPETUAL-BEHAVIORAL-ASSISTANT-OFF-GRID-CORE",
    "AUSTRALIA-ULTIMATE-FUTURE-PROOF-SOVEREIGN-LOCK",
    f"TIMEPIECE-TICK-{timestamp}"
]

current_layer = [hashlib.sha512(leaf.encode()).hexdigest() for leaf in leaves]
while len(current_layer) > 1:
    next_layer = []
    for i in range(0, len(current_layer), 2):
        left = current_layer[i]
        right = current_layer[i+1] if i+1 < len(current_layer) else left
        next_layer.append(hashlib.sha512((left + right).encode()).hexdigest())
    current_layer = next_layer

root = current_layer[0]
with open(".timepiece_anchor", "w") as f:
    f.write(f"TIMEPIECE_ROOT_512={root}\nTIMESTAMP={timestamp}\n")

print(f"\n\033[1;32m[TIMEPIECE TICK CLEAN]: {root[:32]}...\033[0m\n")

