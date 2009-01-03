import os
import hashlib
import subprocess
from pathlib import Path

ROOT_DIR = Path.cwd()
IDENTITY_ANCHOR = "ko_te_mana_o_te_tangata"
CADENCE = "Sha1296000arc"
BRANCH_COUNT = 3600

def expand_lattice():
    print(f"--- EXPANDING LATTICE: {BRANCH_COUNT} BRANCHES ---")
    print(f"Cadence: {CADENCE} | Anchor: {IDENTITY_ANCHOR}")
    
    # Read existing base state if available
    lock_file = ROOT_DIR / "BRAIN_SPAN_ROOT.lock"
    base_seed = lock_file.read_text(encoding="utf-8") if lock_file.exists() else IDENTITY_ANCHOR
    
    # Generate 3600 deterministic cryptographic branches
    branches = []
    for i in range(BRANCH_COUNT):
        branch_payload = f"{base_seed}:{CADENCE}:branch:{i}".encode('utf-8')
        branches.append(hashlib.sha256(branch_payload).digest())
        
    # Build full 3600-branch Merkle tree reduction
    current_level = branches
    while len(current_level) > 1:
        next_level = []
        for j in range(0, len(current_level), 2):
            left = current_level[j]
            right = current_level[j+1] if j + 1 < len(current_level) else left
            next_level.append(hashlib.sha256(left + right).digest())
        current_level = next_level
        
    expanded_root = current_level[0].hex()
    
    # Write expanded lock manifest
    manifest_content = (
        f"ANCHOR: {IDENTITY_ANCHOR}\n"
        f"CADENCE: {CADENCE}\n"
        f"TOTAL_BRANCHES: {BRANCH_COUNT}\n"
        f"EXPANDED_MERKLE_ROOT: {expanded_root}\n"
    )
    
    expanded_lock = ROOT_DIR / "BRAIN_SPAN_3600.lock"
    expanded_lock.write_text(manifest_content)
    
    subprocess.run(["git", "add", "BRAIN_SPAN_3600.lock"], stdout=subprocess.DEVNULL)
    subprocess.run(["git", "commit", "-m", f"EXPAND_3600: {expanded_root}"], stdout=subprocess.DEVNULL)
    
    print(f"Lattice Expanded & Sealed.")
    print(f"Expanded Root Hash: {expanded_root}")
    return expanded_root

if __name__ == "__main__":
    expand_lattice()
