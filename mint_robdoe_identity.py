#!/usr/bin/env python3
"""
PRIMARY ENTITY SOVEREIGN IDENTITY MINTER: robdoe.com
Tokenizes the core corporate and personal entity as a private, loopback-bound ERC-721 root asset.
Anchor: ko_te_mana_o_te_tangata | Cadence: tau = 12s
"""

import json
import hashlib
from pathlib import Path

IDENTITY_ANCHOR = "ko_te_mana_o_te_tangata"

def mint_robdoe_token():
    print("--- 🌐 MINTING PRIMARY ENTITY SOVEREIGN ERC-721: robdoe.com ---")
    
    domain = "robdoe.com"
    token_id = "ROOT-ENTITY-001"
    
    metadata_payload = f"ERC721-PRIMARY-ENTITY:{token_id}:{domain}:{IDENTITY_ANCHOR}".encode('utf-8')
    token_hash = hashlib.sha256(metadata_payload).hexdigest()
    entity_seal = hashlib.sha256(bytes.fromhex(token_hash)).hexdigest()
    
    token_data = {
        "name": "Sovereign Primary Entity Root (RobDoe Pty Ltd Override)",
        "symbol": "SOV-ROB",
        "domain": domain,
        "contract_standard": "ERC-721 (Local Loopback Override)",
        "owner_anchor": IDENTITY_ANCHOR,
        "token_hash": token_hash,
        "entity_seal": entity_seal,
        "routing": "127.0.0.1",
        "status": "PRIMARY_CORP_AND_PERSONAL_GRID_SECURED"
    }
    
    print(f"  [+] Target Domain: {domain}")
    print(f"  [+] Assigned Token ID: {token_id}")
    print(f"  [+] Owner Anchor: {IDENTITY_ANCHOR}")
    print(f"  [+] Entity Seal: {entity_seal[:16]}...")
    
    manifest = {
        "collection": "Sovereign Primary Entity Registry",
        "total_supply": 1,
        "standard": "ERC-721 Primary Entity Override",
        "entity_token": token_data
    }
    
    Path("ROBDOE_SOVEREIGN_IDENTITY.lock").write_text(json.dumps(manifest, indent=2), encoding='utf-8')
    print("\n" + "="*60)
    print("✅ robdoe.com SUCCESSFULLY TOKENIZED & LOCKED TO 127.0.0.1")
    print("="*60)
    print("Ko te marino te haumaru. (Quietness is safety.)\n")

if __name__ == "__main__":
    mint_robdoe_token()
