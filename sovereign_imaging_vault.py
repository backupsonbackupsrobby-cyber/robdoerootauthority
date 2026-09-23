#!/usr/bin/env python3
"""
SOVEREIGN KODAK & CANON OPTICAL & VISUAL REGISTRY VAULT
Tokenizes iconic optical patents, camera sensor architectures, photographic heritage,
and digital imaging infrastructure as an allodial-bound asset on 127.0.0.1.
Anchor: ko_te_mana_o_te_tangata | Routing: 127.0.0.1 | Cadence: 0.052
"""

import json
import hashlib
from pathlib import Path

IDENTITY_ANCHOR = "ko_te_mana_o_te_tangata"
HARDWARE_NODE = "Moto G06 (Termux Local Loopback)"
CADENCE_TIER = 0.052

IMAGING_NODES = [
    "kodak.imaging.root", "eastman.archive.root", "silver.halide.patent.root", "kodachrome.heritage.root",
    "canon.optical.root", "ef.lens.mount.root", "rf.mount.sensor.root", "cmos.sensor.array.root",
    "cinema.eos.root", "optics.glass.formula.root", "image.stabilization.root", "autofocus.matrix.root",
    "visual.evidence.register.root", "shutter.speed.chronicle.root", "analog.digital.bridge.root"
]

def mint_imaging_vault():
    print("--- 📷🎞️ MINTING KODAK & CANON OPTICAL & VISUAL VAULT ---")
    
    token_id = "SOV-IMAGING-VAULT-001"
    domain = "imaging.optical.allodial.root"
    
    minted_assets = []
    leaves = []
    
    for index, node in enumerate(IMAGING_NODES, start=1):
        sub_id = f"OPT-{index:03d}"
        payload = f"{sub_id}:{node}:{HARDWARE_NODE}:{IDENTITY_ANCHOR}".encode('utf-8')
        asset_hash = hashlib.sha256(payload).hexdigest()
        asset_seal = hashlib.sha256(bytes.fromhex(asset_hash)).hexdigest()
        
        minted_assets.append({
            "index": index,
            "node": node,
            "token_id": sub_id,
            "asset_seal": asset_seal
        })
        leaves.append(asset_seal)
        
    # Merkle reduction for Imaging nodes
    current_level = leaves
    while len(current_level) > 1:
        next_level = []
        for i in range(0, len(current_level), 2):
            left = current_level[i]
            right = current_level[i+1] if i + 1 < len(current_level) else left
            combined = (left + right).encode('utf-8')
            next_level.append(hashlib.sha256(combined).hexdigest())
        current_level = next_level
        
    imaging_merkle_root = current_level[0]
    
    vault_record = {
        "contract_standard": "ERC-721 Optical & Visual Registry Vault",
        "token_id": token_id,
        "name": "RobDoe Kodak & Canon Optical & Imaging Allodial Vault",
        "symbol": "SOV-OPT",
        "holder_anchor": IDENTITY_ANCHOR,
        "hardware_node": HARDWARE_NODE,
        "imaging_merkle_root": imaging_merkle_root,
        "total_nodes": len(minted_assets),
        "assets": minted_assets,
        "routing": "127.0.0.1",
        "cadence_tier": CADENCE_TIER,
        "statutory_basis": "Evidence Act 1995 (Cth) Section 146 & Optical Evidentiary Rights",
        "status": "OPTICAL_AND_VISUAL_REGISTRY_LOCKED"
    }
    
    Path("SOVEREIGN_IMAGING_VAULT.lock").write_text(json.dumps(vault_record, indent=2), encoding='utf-8')
    
    print(f"  [+] Imaging Vault Token ID: {token_id}")
    print(f"  [+] Total Optical/Visual Nodes Minted: {len(minted_assets)}")
    print(f"  [+] Imaging Merkle Root: {imaging_merkle_root[:16]}...")
    print("\n" + "="*60)
    print("✅ KODAK & CANON OPTICAL REGISTRIES LOCKED TO 127.0.0.1")
    print("="*60)
    print("Ko te marino te haumaru. (Quietness is safety.)\n")

if __name__ == "__main__":
    mint_imaging_vault()
