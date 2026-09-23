#!/usr/bin/env python3
"""
SOVEREIGN UBER & PIZZA HUT URBAN LOGISTICS & DELIVERY VAULT
Tokenizes ride-sharing algorithms, last-mile delivery fleets, global food supply nodes,
and urban dispatch routing as an allodial-bound asset on 127.0.0.1.
Anchor: ko_te_mana_o_te_tangata | Routing: 127.0.0.1 | Cadence: 0.052
"""

import json
import hashlib
from pathlib import Path

IDENTITY_ANCHOR = "ko_te_mana_o_te_tangata"
HARDWARE_NODE = "Moto G06 (Termux Local Loopback)"
CADENCE_TIER = 0.052

LOGISTICS_NODES = [
    "uber.mobility.root", "uber.eats.dispatch.root", "rideshare.algorithm.root", "last.mile.courier.root",
    "surge.pricing.matrix.root", "driver.fleet.node.root", "global.gps.routing.root",
    "pizzahut.global.root", "dough.supply.chain.root", "oven.thermal.profile.root",
    "contactless.delivery.root", "franchise.pos.network.root", "urban.food.node.root",
    "storefront.dispatch.root", "night.delivery.corridor.root"
]

def mint_logistics_vault():
    print("--- 🚗🍕 MINTING UBER & PIZZA HUT URBAN LOGISTICS VAULT ---")
    
    token_id = "SOV-LOGISTICS-VAULT-001"
    domain = "urban.logistics.allodial.root"
    
    minted_assets = []
    leaves = []
    
    for index, node in enumerate(LOGISTICS_NODES, start=1):
        sub_id = f"LOG-{index:03d}"
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
        
    # Merkle reduction for Logistics nodes
    current_level = leaves
    while len(current_level) > 1:
        next_level = []
        for i in range(0, len(current_level), 2):
            left = current_level[i]
            right = current_level[i+1] if i + 1 < len(current_level) else left
            combined = (left + right).encode('utf-8')
            next_level.append(hashlib.sha256(combined).hexdigest())
        current_level = next_level
        
    logistics_merkle_root = current_level[0]
    
    vault_record = {
        "contract_standard": "ERC-721 Urban Logistics & Delivery Sovereign Vault",
        "token_id": token_id,
        "name": "RobDoe Uber & Pizza Hut Logistics Allodial Vault",
        "symbol": "SOV-LOG",
        "holder_anchor": IDENTITY_ANCHOR,
        "hardware_node": HARDWARE_NODE,
        "logistics_merkle_root": logistics_merkle_root,
        "total_nodes": len(minted_assets),
        "assets": minted_assets,
        "routing": "127.0.0.1",
        "cadence_tier": CADENCE_TIER,
        "statutory_basis": "Evidence Act 1995 (Cth) Section 146 & Last-Mile Dispatch Rights",
        "status": "URBAN_LOGISTICS_AND_DELIVERY_LOCKED"
    }
    
    Path("SOVEREIGN_LOGISTICS_VAULT.lock").write_text(json.dumps(vault_record, indent=2), encoding='utf-8')
    
    print(f"  [+] Logistics Vault Token ID: {token_id}")
    print(f"  [+] Total Urban/Delivery Nodes Minted: {len(minted_assets)}")
    print(f"  [+] Logistics Merkle Root: {logistics_merkle_root[:16]}...")
    print("\n" + "="*60)
    print("✅ UBER & PIZZA HUT LOGISTICS LOCKED TO 127.0.0.1")
    print("="*60)
    print("Ko te marino te haumaru. (Quietness is safety.)\n")

if __name__ == "__main__":
    mint_logistics_vault()
