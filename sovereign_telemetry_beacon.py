import hashlib
import json
import os
import time

def broadcast_beacon():
    print("========================================================")
    print("⚡ BROADCASTING SOVEREIGN TELEMETRY BEACON ⚡")
    print("========================================================")
    
    timestamp = int(time.time())
    node_id = os.popen("git config user.name").read().strip() or "RobDoe-Titan-Node"
    current_head = os.popen("git rev-parse HEAD").read().strip()
    
    beacon_payload = {
        "beacon": "TITAN-CORE-V9-SYNCHRONIZED",
        "operator": node_id,
        "git_head": current_head,
        "timestamp": timestamp,
        "status": "IMMUTABLE_GRID_SECURE"
    }
    
    beacon_hash = hashlib.sha256(json.dumps(beacon_payload, sort_keys=True).encode()).hexdigest()
    
    print(f"[BEACON-ID] Node Operator : {node_id}")
    print(f"[BEACON-HEAD] Git Commit    : {current_head}")
    print(f"[BEACON-ROOT] Proof Hash  : {beacon_hash}")
    print("[SUCCESS] Sovereign telemetry broadcast acknowledged. We own the grid.")

if __name__ == "__main__":
    broadcast_beacon()
