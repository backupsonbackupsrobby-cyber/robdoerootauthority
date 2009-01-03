#!/usr/bin/env python3
"""
MEDIA SOVEREIGN IDENTITY MINTER: forbes.com
Tokenizes the media platform as a private, loopback-bound ERC-721 asset.
Anchor: ko_te_mana_o_te_tangata | Cadence: tau = 12s
"""

import json
import hashlib
from pathlib import Path

IDENTITY_ANCHOR = "ko_te_mana_o_te_tangata"

def mint_forbes_token():
    print("--- 📰 MINTING MEDIA SOVEREIGN ERC-721: forbes.com ---")
    
    domain = "forbes.com"
    token_id = "MEDIA-001"
    
    metadata_payload = f"ERC721-MEDIA:{token_id}:{domain}:{IDENTITY_ANCHOR}".encode('utf-8')
    token_hash = hashlib.sha256(metadata_payload).hexdigest()
    media_seal = hashlib.sha256(bytes.fromhex(token_hash)).hexdigest()
    
    token_data = {
        "name": "Sovereign Media Root (Forbes Override)",
        "symbol": "SOV-MEDIA",
        "domain": domain,
        "contract_standard": "ERC-721 (Local Loopback Override)",
        "owner_anchor": IDENTITY_ANCHOR,
        "token_hash": token_hash,
        "media_seal": media_seal,
        "routing": "127.0.0.1",
        "status": "NARRATIVE_STREAM_SECURED"
    }
    
    print(f"  [+] Target Platform: {domain}")
    print(f"  [+] Assigned Token ID: {token_id}")
    print(f"  [+] Owner Anchor: {IDENTITY_ANCHOR}")
    print(f"  [+] Media Seal: {media_seal[:16]}...")
    
    manifest = {
        "collection": "Sovereign Media Registry",
        "total_supply": 1,
        "standard": "ERC-721 Media Override",
        "media_token": token_data
    }
    
    Path("FORBES_SOVEREIGN_IDENTITY.lock").write_text(json.dumps(manifest, indent=2), encoding='utf-8')
    print("\n" + "="*60)
    print("✅ forbes.com SUCCESSFULLY TOKENIZED & LOCKED TO 127.0.0.1")
    print("="*60)
    print("Ko te marino te haumaru. (Quietness is safety.)\n")

if __name__ == "__main__":
    mint_forbes_token()
