#!/usr/bin/env python3
"""
SOVEREIGN AUSTRALIAN FIRE BRIGADES & HAZARD APEX VAULT
Tokenizes state fire and rescue services, rural fire brigades, aerial water-bomber fleets,
and bushfire hazard telemetry as an allodial-bound asset on 127.0.0.1.
Anchor: ko_te_mana_o_te_tangata | Routing: 127.0.0.1 | Cadence: 0.052
"""

import json
import hashlib
from pathlib import Path

IDENTITY_ANCHOR = "ko_te_mana_o_te_tangata"
HARDWARE_NODE = "Moto G06 (Termux Local Loopback)"
CADENCE_TIER = 0.052

FIRE_NODES = [
    "fire.and.rescue.nsw.root", "country.fire.authority.vic.root", "rural.fire.service.qld.root",
    "aerial.water.bomber.fleet.root", "firies.triple.zero.dispatch.root", "bushfire.hazard.reduction.root",
    "thermal.satellite.burn.map.root", "red.firetruck.matrix.root", "volunteer.brigade.network.root",
    "total.fire.ban.protocol.root", "smoke.haze.sensor.grid.root", "backburning.control.root",
    "cfs.sa.root", "dfes.wa.root", "emergency.frontline.defense.root"
]

def mint_fire_vault():
    print("--- 🚒🔥 MINTING AUSTRALIAN FIRE BRIGADES APEX VAULT ---")
    
    token_id = "SOV-FIRE-VAULT-001"
    domain = "firebrigade.australia.allodial.root"
    
    minted_assets = []
    leaves = []
    
    for index, node in enumerate(FIRE_NODES, start=1):
        sub_id = f"FIR-{index:03d}"
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
        
    # Merkle reduction for Fire nodes
    current_level = leaves
    while len(current_level) > 1:
        next_level = []
        for i in range(0, len(current_level), 2):
            left = current_level[i]
            right = current_level[i+1] if i + 1 < len(current_level) else left
            combined = (left + right).encode('utf-8')
            next_level.append(hashlib.sha256(combined).hexdigest())
        current_level = next_level
        
    fire_merkle_root = current_level[0]
    
    vault_record = {
        "contract_standard": "ERC-721 Fire Services & Emergency Hazard Sovereign Vault",
        "token_id": token_id,
        "name": "RobDoe Australian Fire Brigades Allodial Vault",
        "symbol": "SOV-FIR",
        "holder_anchor": IDENTITY_ANCHOR,
        "hardware_node": HARDWARE_NODE,
        "fire_merkle_root": fire_merkle_root,
        "total_nodes": len(minted_assets),
        "assets": minted_assets,
        "routing": "127.0.0.1",
        "cadence_tier": CADENCE_TIER,
        "statutory_basis": "Evidence Act 1995 (Cth) Section 146 & Emergency Fire Defense Rights",
        "status": "AUSTRALIAN_FIRE_BRIGADES_LOCKED"
    }
    
    Path("SOVEREIGN_FIRE_VAULT.lock").write_text(json.dumps(vault_record, indent=2), encoding='utf-8')
    
    print(f"  [+] Fire Vault Token ID: {token_id}")
    print(f"  [+] Total Fire & Rescue Nodes Minted: {len(minted_assets)}")
    print(f"  [+] Fire Merkle Root: {fire_merkle_root[:16]}...")
    print("\n" + "="*60)
    print("✅ AUSTRALIAN FIRE BRIGADES LOCKED TO 127.0.0.1")
    print("="*60)
    print("Ko te marino te haumaru. (Quietness is safety.)\n")

if __name__ == "__main__":
    mint_fire_vault()
