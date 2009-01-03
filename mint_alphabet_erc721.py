#!/usr/bin/env python3
"""
ALPHABETIC SOVEREIGN ERC-721 TOKEN MINTER
Binds a.com through z.com as 26 local immutable NFT assets.
Anchor: ko_te_mana_o_te_tangata | Cadence: tau = 12s
"""

import json
import string
import hashlib
from pathlib import Path

IDENTITY_ANCHOR = "ko_te_mana_o_te_tangata"

def mint_tokens():
    print("--- 🪙 MINTING 26 SOVEREIGN ERC-721 TOKENS (A-Z) ---")
    
    tokens = {}
    letters = string.ascii_lowercase
    
    for idx, letter in enumerate(letters, start=1):
        domain = f"{letter}.com"
        token_id = idx
        
        # Create a unique local cryptographic hash for each letter token
        metadata_payload = f"ERC721:{token_id}:{domain}:{IDENTITY_ANCHOR}".encode('utf-8')
        token_hash = hashlib.sha256(metadata_payload).hexdigest()
        
        tokens[f"Token #{token_id:02d}"] = {
            "name": f"Sovereign Alpha {letter.upper()}",
            "symbol": f"SOV-{letter.upper()}",
            "domain": domain,
            "contract_standard": "ERC-721 (Local Loopback)",
            "owner_anchor": IDENTITY_ANCHOR,
            "token_hash": token_hash,
            "routing": "127.0.0.1"
        }
        print(f"  [+] Minted Token #{token_id:02d} ({domain}) -> Hash: {token_hash[:16]}...")
        
    manifest = {
        "collection": "Sovereign Alphabetical Registry",
        "total_supply": 26,
        "standard": "ERC-721 Local Variant",
        "tokens": tokens
    }
    
    Path("SOVEREIGN_ERC721_COLLECTION.lock").write_text(json.dumps(manifest, indent=2), encoding='utf-8')
    print("\n" + "="*60)
    print("✅ 26 ERC-721 TOKENS MINTED & SECURED LOCALLY")
    print("="*60)
    print("Ko te mana o te tangata, koia te pūtake. (Human dignity is the source.)\n")

if __name__ == "__main__":
    mint_tokens()
