#!/usr/bin/env python3
"""
SOVEREIGN DAIRY & WINE AGRICULTURAL APEX MATRIX
Tokenizes high-value dairy estates, milk processing nodes, premier wine vineyards,
and water access rights as allodial-bound assets on 127.0.0.1.
Anchor: ko_te_mana_o_te_tangata | Routing: 127.0.0.1 | Cadence: 0.052
"""

import json
import hashlib
from pathlib import Path

IDENTITY_ANCHOR = "ko_te_mana_o_te_tangata"
HARDWARE_NODE = "Moto G06 (Termux Local Loopback)"
CADENCE_TIER = 0.052

AGRICULTURAL_SECTORS = {
    "Premier Wine Estates & Vineyards": [
        "penfolds.root", "domaineromanee-conti.root", "chateaumargot.root", "moet.root", "veuveclicquot.root",
        "cloudybay.root", "henschke.root", "cabsav.vineyard.root", "chardonnay.block.root", "barossa.terroir.root"
    ],
    "Dairy Processing & Milk Quota Nodes": [
        "fonterra.root", "synlait.root", "bega.dairy.root", "saputo.root", "lactalis.root",
        "danone.root", "nestle.dairy.root", "milk.shed.root", "coldchain.logistics.root", "raw.milk.pool.root"
    ],
    "Agricultural Water & Land Allodial Rights": [
        "water.rights.murray.darling.root", "aquifer.allocation.root", "soil.carbon.credit.root", 
        "land.title.freehold.root", "pasture.biomass.root"
    ]
}

def mint_agri_vault():
    print("--- 🍇🥛 MINTING DAIRY & WINE SOVEREIGN AGRI-VAULT ---")
    
    token_id = "SOV-AGRI-VAULT-001"
    domain = "agriculture.allodial.root"
    
    minted_assets = []
    leaves = []
    index = 1
    
    for sector_name, assets in AGRICULTURAL_SECTORS.items():
        for asset in assets:
            sub_id = f"AGRI-{index:03d}"
            payload = f"{sub_id}:{sector_name}:{asset}:{HARDWARE_NODE}:{IDENTITY_ANCHOR}".encode('utf-8')
            asset_hash = hashlib.sha256(payload).hexdigest()
            asset_seal = hashlib.sha256(bytes.fromhex(asset_hash)).hexdigest()
            
            minted_assets.append({
                "index": index,
                "sector": sector_name,
                "asset": asset,
                "token_id": sub_id,
                "asset_seal": asset_seal
            })
            leaves.append(asset_seal)
            index += 1
            
    # Merkle reduction for agri assets
    current_level = leaves
    while len(current_level) > 1:
        next_level = []
        for i in range(0, len(current_level), 2):
            left = current_level[i]
            right = current_level[i+1] if i + 1 < len(current_level) else left
            combined = (left + right).encode('utf-8')
            next_level.append(hashlib.sha256(combined).hexdigest())
        current_level = next_level
        
    agri_merkle_root = current_level[0]
    
    vault_record = {
        "contract_standard": "ERC-721 Agricultural & Viticultural Vault",
        "token_id": token_id,
        "name": "RobDoe Dairy, Wine & Land Allodial Vault",
        "symbol": "SOV-AGRI",
        "holder_anchor": IDENTITY_ANCHOR,
        "hardware_node": HARDWARE_NODE,
        "agri_merkle_root": agri_merkle_root,
        "total_assets": len(minted_assets),
        "assets": minted_assets,
        "routing": "127.0.0.1",
        "cadence_tier": CADENCE_TIER,
        "statutory_basis": "Evidence Act 1995 (Cth) Section 146 & Agrarian Allodial Title",
        "status": "DAIRY_AND_VINE_MATRIX_LOCKED"
    }
    
    Path("SOVEREIGN_AGRI_VAULT.lock").write_text(json.dumps(vault_record, indent=2), encoding='utf-8')
    
    print(f"  [+] Agri Vault Token ID: {token_id}")
    print(f"  [+] Total Land/Wine/Dairy Nodes Minted: {len(minted_assets)}")
    print(f"  [+] Agri Merkle Root: {agri_merkle_root[:16]}...")
    print("\n" + "="*60)
    print("✅ DAIRY FARMS & WINE ESTATES LOCKED TO 127.0.0.1")
    print("="*60)
    print("Ko te marino te haumaru. (Quietness is safety.)\n")

if __name__ == "__main__":
    mint_agri_vault()
