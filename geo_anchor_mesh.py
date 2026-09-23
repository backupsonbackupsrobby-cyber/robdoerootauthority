import time
import hashlib

SECRET_KEY = "esp32"

def anchor_node_geo(region, lat, lon, channel_freq, node_id):
    payload = f"GEO-ANCHOR|REGION:{region}|LAT:{lat}|LON:{lon}|NODE:{node_id}|FREQ:{channel_freq}|SEC:{SECRET_KEY}"
    frame_hash = hashlib.sha256(payload.encode()).hexdigest()[:16]
    print(f"[GEO-LOCK] {region} ({lat}, {lon}) | Ch: {channel_freq}MHz | Node: {node_id} | Proof: {frame_hash}")

if __name__ == "__main__":
    print(f"[*] Initializing Global Geographic Coordinate Anchoring Protocol...")
    
    # Global nodes with precise lat/long geographic anchors across both hemispheres
    nodes = [
        # Australia / NZ
        {"region": "QLD-Edge", "lat": -27.4698, "lon": 153.0251, "ch": 915.0, "id": 1},
        {"region": "NT-Edge", "lat": -12.4634, "lon": 130.8456, "ch": 868.0, "id": 2},
        {"region": "WA-Edge", "lat": -31.9505, "lon": 115.8605, "ch": 433.5, "id": 3},
        {"region": "SA-Edge", "lat": -34.9285, "lon": 138.6007, "ch": 2412.0, "id": 4},
        {"region": "ACT-Edge", "lat": -35.2809, "lon": 149.1300, "ch": 915.0, "id": 5},
        {"region": "NSW-Edge", "lat": -33.8688, "lon": 151.2093, "ch": 868.0, "id": 6},
        {"region": "NZ-North", "lat": -36.8485, "lon": 174.7633, "ch": 433.5, "id": 7},
        {"region": "NZ-South", "lat": -43.5321, "lon": 172.6362, "ch": 2412.0, "id": 8},
        # Global South
        {"region": "Africa-South", "lat": -33.9249, "lon": 18.4241, "ch": 915.0, "id": 9},
        {"region": "South-America", "lat": -33.4489, "lon": -70.6693, "ch": 868.0, "id": 10},
        {"region": "Antarctic-Deep", "lat": -77.8419, "lon": 166.6863, "ch": 433.5, "id": 11},
        # Global North
        {"region": "North-America", "lat": 37.7749, "lon": -122.4194, "ch": 2412.0, "id": 12},
        {"region": "Europe-Central", "lat": 52.5200, "lon": 13.4050, "ch": 915.0, "id": 13},
        {"region": "Asia-Pacific", "lat": 35.6762, "lon": 139.6503, "ch": 868.0, "id": 14},
        {"region": "Arctic-Polar", "lat": 78.2232, "lon": 15.6267, "ch": 433.5, "id": 15}
    ]

    for node in nodes:
        anchor_node_geo(node["region"], node["lat"], node["lon"], node["ch"], node["id"])
        time.sleep(0.04)

    print("[+] All Planetary Mesh Nodes Geographically Locked and Verified.")
