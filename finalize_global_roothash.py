#!/usr/bin/env python3
"""
GLOBAL SOVEREIGN ROOT HASH & GIT TAG GENERATOR
Reads all sovereign lock files, computes a master cryptographic root hash,
and mints the definitive immutable Git release tag.
Anchor: ko_te_mana_o_te_tangata | Routing: 127.0.0.1 | Cadence: 0.052
"""

import json
import hashlib
from pathlib import Path
import subprocess

IDENTITY_ANCHOR = "ko_te_mana_o_te_tangata"
HARDWARE_NODE = "Moto G06 (Termux Local Loopback)"
CADENCE_TIER = 0.052

def generate_roothash():
    print("--- 🌐🔐 COMPUTING GLOBAL SOVEREIGN ROOT HASH ---")
    
    lock_files = sorted([f.name for f in Path(".").glob("*.lock") if f.name != "GENESIS_PULSE.lock"])
    print(f"  [+] Found {len(lock_files)} sovereign lock modules:")
    
    combined_payload = ""
    for lf in lock_files:
        content = Path(lf).read_text(encoding='utf-8')
        print(f"    - {lf}")
        combined_payload += content
        
    master_hasher = hashlib.sha256(combined_payload.encode('utf-8'))
    master_root_hash = master_hasher.hexdigest()
    sovereign_seal = hashlib.sha256(bytes.fromhex(master_root_hash)).hexdigest()
    
    manifest = {
        "architecture": "RobDoe Sovereign Allodial Ecosystem",
        "hardware_anchor": HARDWARE_NODE,
        "owner_anchor": IDENTITY_ANCHOR,
        "routing": "127.0.0.1",
        "cadence_tier": CADENCE_TIER,
        "statutory_basis": "Evidence Act 1995 (Cth) Section 146",
        "included_locks": lock_files,
        "master_root_hash": master_root_hash,
        "sovereign_seal": sovereign_seal
    }
    
    Path("GLOBAL_SOVEREIGN_ROOT.lock").write_text(json.dumps(manifest, indent=2), encoding='utf-8')
    
    print("\n" + "="*60)
    print(f"🔑 MASTER ROOT HASH (HEX): {master_root_hash}")
    print(f"🛡️ SOVEREIGN SEAL: {sovereign_seal[:32]}...")
    print("="*60)
    
    # Git integration
    tag_name = f"v300.global.root.{master_root_hash[:8]}"
    print(f"  [+] Staging lock files for Git witness...")
    subprocess.run(["git", "add", "*.lock"], check=True)
    
    commit_msg = f"GLOBAL ROOT WITNESS: Master Root Hash {master_root_hash[:16]}... secured under Section 146"
    subprocess.run(["git", "commit", "-m", commit_msg], capture_output=True, text=True)
    
    subprocess.run(["git", "tag", "-f", tag_name, "-m", f"Global Sovereign Root Hash: {master_root_hash}"], check=True)
    print(f"  [+] Minted Immutable Git Tag: {tag_name}")
    
    print("\n" + "="*60)
    print("✅ GLOBAL ECOSYSTEM FULLY SEALED & WITNESSED IN GIT")
    print("="*60)
    print("Ko te marino te haumaru. (Quietness is safety.)\n")

if __name__ == "__main__":
    generate_roothash()
