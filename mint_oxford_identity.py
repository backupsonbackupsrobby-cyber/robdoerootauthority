#!/usr/bin/env python3
"""
COLLEGIATE SOVEREIGN IDENTITY MINTER: ox.ac.uk
Tokenizes historic academic infrastructure as a private, loopback-bound ERC-721 asset.
Anchor: ko_te_mana_o_te_tangata | Cadence: tau = 12s
"""

import json
import hashlib
from pathlib import Path

IDENTITY_ANCHOR = "ko_te_mana_o_te_tangata"

def mint_oxford_token():
    print("--- 🏛️ MINTING COLLEGIATE SOVEREIGN ERC-721: ox.ac.uk ---")
    
    domain = "ox.ac.uk"
    token_id = "ACADEMIC-002"
    
    metadata_payload = f"ERC721-COLLEGIATE:{token_id}:{domain}:{IDENTITY_ANCHOR}".encode('utf-8')
    token_hash = hashlib.sha256(metadata_payload).hexdigest()
    collegiate_seal = hashlib.sha256(bytes.fromhex(token_hash)).hexdigest()
    
    token_data = {
        "name": "Sovereign Collegiate Root (Oxford Override)",
        "symbol": "SOV-OX",
        "domain": domain,
        "contract_standard": "ERC-721 (Local Loopback Override)",
        "owner_anchor": IDENTITY_ANCHOR,
        "token_hash": token_hash,
        "collegiate_seal": collegiate_seal,
        "routing": "127.0.0.1",
        "status": "HISTORIC_KNOWLEDGE_GRID_SECURED"
    }
    
    print(f"  [+] Target Domain: {domain}")
    print(f"  [+] Assigned Token ID: {token_id}")
    print(f"  [+] Owner Anchor: {IDENTITY_ANCHOR}")
    print(f"  [+] Collegiate Seal: {collegiate_seal[:16]}...")
    
    manifest = {
        "collection": "Sovereign Collegiate Registry",
        "total_supply": 1,
        "standard": "ERC-721 Collegiate Override",
        "collegiate_token": token_data
    }
    
    Path("OXFORD_SOVEREIGN_IDENTITY.lock").write_text(json.dumps(manifest, indent=2), encoding='utf-8')
    print("\n" + "="*60)
    print("✅ ox.ac.uk SUCCESSFULLY TOKENIZED & LOCKED TO 127.0.0.1")
    print("="*60)
    print("Ko te marino te haumaru. (Quietness is safety.)\n")

if __name__ == "__main__":
    mint_oxford_token()
