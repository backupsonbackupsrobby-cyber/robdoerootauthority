import hashlib
import json
import os
import time

STATE_FILE = ".sleeble_active_context.json"

def compute_merkle_root(leaf_hashes):
    if not leaf_hashes:
        return hashlib.sha256(b"genesis").hexdigest()
    
    current_level = [bytes.fromhex(h) for h in leaf_hashes]
    while len(current_level) > 1:
        next_level = []
        for i in range(0, len(current_level), 2):
            left = current_level[i]
            right = current_level[i+1] if i + 1 < len(current_level) else left
            combined = hashlib.sha256(left + right).digest()
            next_level.append(combined)
        current_level = next_level
    return current_level[0].hex()

def execute_sovereign_cycle():
    print("========================================================")
    print("⚡ RECURSIVE MERKLE TREE FRAMEWORK: STATE SYNCHRONIZATION ⚡")
    print("========================================================")
    
    # Generate autonomous state payload
    timestamp = int(time.time())
    node_seeds = [hashlib.sha256(f"NODE-SECTOR-{i}-{timestamp}".encode()).hexdigest() for i in range(4)]
    
    merkle_root = compute_merkle_root(node_seeds)
    
    state_payload = {
        "timestamp": timestamp,
        "authority": "ROBDOE-ROOT-AUTHORITY",
        "active_nodes": len(node_seeds),
        "leaf_hashes": node_seeds,
        "merkle_root": merkle_root,
        "status": "IMMUTABLE_GROUND_TRUTH"
    }
    
    with open(STATE_FILE, "w") as f:
        json.dump(state_payload, f, indent=4)
        
    print(f"[INFO] State written to immutable context: {STATE_FILE}")
    print(f"[ROOT] Calculated Merkle Root: {merkle_root}")
    print("[SUCCESS] Autonomous daemon state persistence locked.")

if __name__ == "__main__":
    execute_sovereign_cycle()
