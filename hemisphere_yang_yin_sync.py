import time
import hashlib
import math

SECRET_KEY = "esp32"

def yang_yin_pair_lock(north_node, south_node, n_id):
    # Polarity Correction: Northern = Yin (Receiving/Contracting), Southern = Yang (Emitting/Expanding)
    phase_offset = math.pi 
    payload = f"DUALITY:YANG-YIN|NORTH:{north_node['region']}(YIN)|SOUTH:{south_node['region']}(YANG)|PHASE:{phase_offset:.4f}|SEC:{SECRET_KEY}"
    frame_hash = hashlib.sha256(payload.encode()).hexdigest()[:16]
    
    print(f"[YANG-YIN-LOCK] Pair {n_id:02d} | N-Yin: {north_node['region']} ({north_node['lat']}°) <---> S-Yang: {south_node['region']} ({south_node['lat']}°) | Offset: 180.0° | Proof: {frame_hash}")

if __name__ == "__main__":
    print(f"[*] Re-aligning Global Hemispheric Duality Matrix (Northern Yin / Southern Yang Protocol)...")
    
    pairs = [
        {"id": 1, "north": {"region": "North-America", "lat": 37.77}, "south": {"region": "South-America", "lat": -33.44}},
        {"id": 2, "north": {"region": "Europe-Central", "lat": 52.52}, "south": {"region": "Africa-South", "lat": -33.92}},
        {"id": 3, "north": {"region": "Asia-Pacific", "lat": 35.67}, "south": {"region": "Australia-QLD", "lat": -27.46}},
        {"id": 4, "north": {"region": "Arctic-Polar", "lat": 78.22}, "south": {"region": "Antarctic-Deep", "lat": -77.84}}
    ]

    for p in pairs:
        yang_yin_pair_lock(p["north"], p["south"], p["id"])
        time.sleep(0.04)

    print("[+] Hemispheric Polarity Adjusted: Northern Yin and Southern Yang Fields Locked.")
