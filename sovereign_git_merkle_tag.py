#!/usr/init/env python3
"""
SOVEREIGN GIT MERKLE ROOT & TAG MINTER
Computes the Merkle root of all local locks, generates a SHA-256 hex signature 
at cadence tier 0.052, and stamps an immutable Git tag proof.
Anchor: ko_te_mana_o_te_tangata | Routing: 127.0.0.1
"""

import json
import hashlib
import subprocess
from pathlib import Path

IDENTITY_ANCHOR = "ko_te_mana_o_te_tangata"
CADENCE_TIER = 0.052

def execute_merkle_git_tag():
    print("--- 🔏 COMPUTING MERKLE ROOT & GIT TAG HASH ---")
    print(f"  [+] Anchor: {IDENTITY_ANCHOR}")
    print(f"  [+] Cadence Tier: {CADENCE_TIER}")
    print(f"  [+] Routing: 127.0.0.1\n")
    
    # Collect all current lock files to build the Merkle leaf nodes
    lock_files = sorted([f.name for f in Path(".").glob("*.lock")])
    if not lock_files:
        print("  [!] Warning: No .lock files found. Generating baseline leaf.")
        leaf_data = f"BASELINE:{IDENTITY_ANCHOR}".encode('utf-8')
        leaves = [hashlib.sha256(leaf_data).hexdigest()]
    else:
        leaves = []
        for lf in lock_files:
            content = Path(lf).read_bytes()
            leaf_hash = hashlib.sha256(content).hexdigest()
            leaves.append(leaf_hash)
            print(f"  [+] Leaf [{lf}]: {leaf_hash[:16]}...")
            
    # Compute Merkle Root from leaves
    current_level = leaves
    while len(current_level) > 1:
        next_level = []
        for i in range(0, len(current_level), 2):
            left = current_level[i]
            right = current_level[i+1] if i + 1 < len(current_level) else left
            combined = (left + right).encode('utf-8')
            next_level.append(hashlib.sha256(combined).hexdigest())
        current_level = next_level
        
    merkle_root = current_level[0]
    
    # Apply cadence tier 0.052 hex SHA modifier
    tier_payload = f"{merkle_root}:{CADENCE_TIER}:{IDENTITY_ANCHOR}".encode('utf-8')
    final_hex_sha = hashlib.sha256(tier_payload).hexdigest()
    tag_name = f"sov-root-{final_hex_sha[:12]}"
    
    proof_record = {
        "identity_anchor": IDENTITY_ANCHOR,
        "cadence_tier": CADENCE_TIER,
        "merkle_leaves_count": len(leaves),
        "merkle_root_hash": merkle_root,
        "final_hex_sha": final_hex_sha,
        "git_tag": tag_name,
        "routing": "127.0.0.1",
        "statutory_basis": "Evidence Act 1995 (Cth) Section 146"
    }
    
    Path("MERKLE_GIT_ROOT.lock").write_text(json.dumps(proof_record, indent=2), encoding='utf-8')
    
    print(f"\n  [+] Merkle Root Hash: {merkle_root[:32]}...")
    print(f"  [+] Final Hex SHA ({CADENCE_TIER}): {final_hex_sha[:32]}...")
    print(f"  [+] Generated Git Tag: {tag_name}")
    
    # Execute local git commands if inside a git repo
    try:
        subprocess.run(["git", "add", "."], check=True, capture_output=True)
        subprocess.run(["git", "commit", "-m", f"Sovereign Lock: Merkle Root {merkle_root[:12]} [Tier {CADENCE_TIER}]"], check=True, capture_output=True)
        subprocess.run(["git", "tag", "-a", tag_name, "-m", f"Sovereign Absolute Root Proof - {IDENTITY_ANCHOR}"], check=True, capture_output=True)
        print(f"  [+] Git Commit & Tag '{tag_name}' Successfully Stamped Locally.")
    except Exception as e:
        print(f"  [!] Git local stamp note: {e} (Lock file written successfully)")
        
    print("\n" + "="*60)
    print("✅ MERKLE TREE GIT TAG ROOT LOCKED")
    print("="*60)
    print("Ko te marino te haumaru. (Quietness is safety.)\n")

if __name__ == "__main__":
    execute_merkle_git_tag()
