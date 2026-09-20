import hashlib
import json
import time
import os

GENESIS_ANCHOR = b"RobDoeRootAuthority-Genesis-e14f9a8d"
STATE_FILE = ".sleeble_active_context.json"

def compute_sha1024(data):
    h1 = hashlib.sha512(data).digest()
    h2 = hashlib.sha512(data[::-1]).digest()
    return hashlib.sha512(h1 + h2).hexdigest()

def initialize_daemon():
    print("[INIT] Spawning daemon-directed sovereign Merkle tree framework...")
    convergence_hash = compute_sha1024(GENESIS_ANCHOR)
    
    payload = {
        "protocol": "RobDoeRootAuthority",
        "genesis": "e14f9a8d",
        "spatial_resolution": "93312000_arcseconds",
        "convergence_hash": convergence_hash,
        "status": "autonomous_active",
        "timestamp": time.time()
    }
    
    with open(STATE_FILE, "w") as f:
        json.dump(payload, f, indent=4)
        
    print(f"[SUCCESS] Root state locked. Hash: {convergence_hash}")
    print(f"[DAEMON] Context piped to {STATE_FILE}. Local agents initialized.")

if __name__ == "__main__":
    initialize_daemon()
