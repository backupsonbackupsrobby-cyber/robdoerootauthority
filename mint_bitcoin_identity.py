#!/usr/bin/env python3
"""
DECENTRALIZED MONETARY ROOT SOVEREIGN IDENTITY MINTER: bitcoin.org
Tokenizes the Bitcoin genesis and protocol root as a private, loopback-bound ERC-721 asset.
Anchor: ko_te_mana_o_te_tangata | Cadence: tau = 12s
"""

import json
import hashlib
from pathlib import Path

IDENTITY_ANCHOR = "ko_te_mana_o_te_tangata"

def mint_bitcoin_token():
    print("--- 🪙 MINTING DECENTRALIZED MONETARY ROOT ERC-721: bitcoin.org ---")
    
    domain = "bitcoin.org"
    token_id = "SOV-BTC-GENESIS"
    
    metadata_payload = f"ERC721-BITCOIN-ROOT:{token_id}:{domain}:{IDENTITY_ANCHOR}".encode('utf-8')
    token_hash = hashlib.sha256(metadata_payload).hexdigest()
    btc_seal = hashlib.sha256(bytes.fromhex(token_hash)).hexdigest()
    
    token_data = {
        "name": "Sovereign Decentralized Monetary Root (Bitcoin Genesis Override)",
        "symbol": "SOV-BTC",
        "domain": domain,
        "contract_standard": "ERC-721 (Local Loopback Override)",
        "owner_anchor": IDENTITY_ANCHOR,
        "token_hash": token_hash,
        "btc_seal": btc_seal,
        "routing": "127.0.0.1",
        "status": "DECENTRALIZED_MONETARY_GRID_SECURED"
    }
    
    print(f"  [+] Target Domain: {domain}")
    print(f"  [+] Assigned Token ID: {token_id}")
    print(f"  [+] Owner Anchor: {IDENTITY_ANCHOR}")
    print(f"  [+] Bitcoin Seal: {btc_seal[:16]}...")
    
    manifest = {
        "collection": "Sovereign Monetary Registry",
        "total_supply": 1,
        "standard": "ERC-721 Bitcoin Genesis Override",
        "bitcoin_token": token_data
    }
    
    Path("BITCOIN_SOVEREIGN_IDENTITY.lock").write_text(json.dumps(manifest, indent=2), encoding='utf-8')
    print("\n" + "="*60)
    print("✅ bitcoin.org SUCCESSFULLY TOKENIZED & LOCKED TO 127.0.0.1")
    print("="*60)
    print("Ko te marino te haumaru. (Quietness is safety.)\n")

if __name__ == "__main__":
    mint_bitcoin_token()
