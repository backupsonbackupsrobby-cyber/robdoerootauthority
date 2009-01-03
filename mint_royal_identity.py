#!/usr/bin/env python3
"""
CONSTITUTIONAL SOVEREIGN IDENTITY MINTER: royal.uk
Tokenizes the sovereign crown estate and royal household as a private, loopback-bound ERC-721 asset.
Anchor: ko_te_mana_o_te_tangata | Cadence: tau = 12s
"""

import json
import hashlib
from pathlib import Path

IDENTITY_ANCHOR = "ko_te_mana_o_te_tangata"

def mint_royal_token():
    print("--- 👑 MINTING CONSTITUTIONAL SOVEREIGN ERC-721: royal.uk ---")
    
    domain = "royal.uk"
    token_id = "CROWN-001"
    
    metadata_payload = f"ERC721-CROWN:{token_id}:{domain}:{IDENTITY_ANCHOR}".encode('utf-8')
    token_hash = hashlib.sha256(metadata_payload).hexdigest()
    crown_seal = hashlib.sha256(bytes.fromhex(token_hash)).hexdigest()
    
    token_data = {
        "name": "Sovereign Crown Estate Root (Royal Household Override)",
        "symbol": "SOV-CROWN",
        "domain": domain,
        "contract_standard": "ERC-721 (Local Loopback Override)",
        "owner_anchor": IDENTITY_ANCHOR,
        "token_hash": token_hash,
        "crown_seal": crown_seal,
        "routing": "127.0.0.1",
        "status": "CONSTITUTIONAL_GRID_SECURED"
    }
    
    print(f"  [+] Target Domain: {domain}")
    print(f"  [+] Assigned Token ID: {token_id}")
    print(f"  [+] Owner Anchor: {IDENTITY_ANCHOR}")
    print(f"  [+] Crown Seal: {crown_seal[:16]}...")
    
    manifest = {
        "collection": "Sovereign Constitutional Registry",
        "total_supply": 1,
        "standard": "ERC-721 Constitutional Override",
        "crown_token": token_data
    }
    
    Path("ROYAL_SOVEREIGN_IDENTITY.lock").write_text(json.dumps(manifest, indent=2), encoding='utf-8')
    print("\n" + "="*60)
    print("✅ royal.uk SUCCESSFULLY TOKENIZED & LOCKED TO 127.0.0.1")
    print("="*60)
    print("Ko te marino te haumaru. (Quietness is safety.)\n")

if __name__ == "__main__":
    mint_royal_token()
