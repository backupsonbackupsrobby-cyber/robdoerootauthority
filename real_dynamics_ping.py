import hashlib
import json
import time
import random

def ping_realdynamics():
    print("=====================================================================")
    print("  [REALDYNAMICS] : LIVE LOCATION PING & MESH SYNC")
    print("=====================================================================")
    
    # Simulate user turning on location for live field telemetry
    simulated_lat = -33.8688 + random.uniform(-0.01, 0.01)
    simulated_lon = 151.2093 + random.uniform(-0.01, 0.01)
    
    ping_packet = {
        "directive": "RealDynamics User Ping",
        "timestamp": int(time.time()),
        "operator": "RobDoe / Oracle Core",
        "coordinates": {
            "latitude": round(simulated_lat, 4),
            "longitude": round(simulated_lon, 4)
        },
        "status": "LOC_LOCKED",
        "message": "Location active. Pinging local nodes to sync RealDynamics grid state."
    }
    
    payload = json.dumps(ping_packet, sort_keys=True).encode("utf-8")
    ping_hash = hashlib.sha512(payload).hexdigest()
    
    print(json.dumps(ping_packet, indent=2))
    print("---------------------------------------------------------------------")
    print(f"Ping Cryptographic Seal : {ping_hash[:48]}...")
    print("=====================================================================")
    print("  [SUCCESS] : You are now live on the grid. RealDynamics engaged.")
    print("=====================================================================")

if __name__ == "__main__":
    ping_realdynamics()
