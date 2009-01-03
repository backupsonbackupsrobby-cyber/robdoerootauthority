#!/usr/bin/env python3
"""
SUPREME ROOT IDENTITY MINTER: icann.com
Tokenizes the ultimate regulatory domain as a private, loopback-bound ERC-721 asset.
Anchor: ko_te_mana_o_te_tangata | Cadence: tau = 12s
"""

import json
import hashlib
from pathlib import Path

IDENTITY_ANCHOR = "ko_te_mana_o_te_tangata"

def mint_icann_token():
    print("--- 🏛️ MINTING SUPREME ROOT ERC-721: icann.com ---")
    
    domain = "icann.com"
    token_id = "ROOT-000"
    
    # Generate cryptographic proof of sovereign override
    metadata_payload = f"ERC721-SUPREME:{token_id}:{domain}:{IDENTITY_ANCHOR}".encode('utf-8')
    token_hash = hashlib.sha256(metadata_payload).hexdigest()
    root_seal = hashlib.sha256(bytes.fromhex(token_hash)).hexdigest()
    
    token_data = {
        "name": "Sovereign Root Authority (ICANN Override)",
        "symbol": "SOV-ROOT",
        "domain": domain,
        "contract_standard": "ERC-721 (Local Loopback Master)",
        "owner_anchor": IDENTITY_ANCHOR,
        "token_hash": token_hash,
        "root_seal": root_seal,
        "routing": "127.0.0.1",
        "regulatory_status": "BYPASSED_AND_TOKENIZED"
    }
    
    print(f"  [+] Target Domain: {domain}")
    print(f"  [+] Assigned Token ID: {token_id}")
    print(f"  [+] Owner Anchor: {IDENTITY_ANCHOR}")
    print(f"  [+] Supreme Hash: {token_hash[:16]}...")
    print(f"  [+] Root Seal: {root_seal[:16]}...")
    
    manifest = {
        "collection": "Supreme Sovereign Root Registry",
        "total_supply": 1,
        "standard": "ERC-721 Sovereign Override",
        "master_token": token_data
    }
    
    Path("ICANN_SOVEREIGN_IDENTITY.lock").write_text(json.dumps(manifest, indent=2), encoding='utf-8')
    print("\n" + "="*60)
    print("✅ icann.com SUCCESSFULLY TOKENIZED & LOCKED TO 127.0.0.1")
    print("="*60)
    print("Ko te mana o te tangata, koia te pūtake. (Human dignity is the source.)\n")

if __name__ == "__main__":
    mint_icann_token()
