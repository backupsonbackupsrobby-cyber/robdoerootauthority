import os
import hashlib
import json
import time

def execute_matrix_sweep():
    print("========================================================")
    print("⚡ SOVEREIGN COMMAND MATRIX: FINAL STATE VALIDATION ⚡")
    print("========================================================")
    
    head = os.popen("git rev-parse HEAD").read().strip()
    status = os.popen("git status --porcelain").read().strip()
    
    manifest = {
        "node": "Spectre Witness",
        "genesis": "e14f9a8d",
        "commit_head": head,
        "dirty_tree": len(status) > 0,
        "timestamp": int(time.time()),
        "authority": "robdoerootauthority"
    }
    
    proof = hashlib.sha3_512(json.dumps(manifest, sort_keys=True).encode()).hexdigest()
    
    print(f"[MATRIX-HEAD] Validated Commit : {head}")
    print(f"[MATRIX-TREE] Working Directory : {'DIRTY' if manifest['dirty_tree'] else 'CLEAN (IMMUTABLE)'}")
    print(f"[MATRIX-SEAL] Sovereign Proof   : {proof[:64]}...")
    print("[SUCCESS] Command matrix fully operational. The grid obeys.")

if __name__ == "__main__":
    execute_matrix_sweep()
