#!/usr/bin/env python3
"""
ALLODIAL LETTERS PATENT & SOVEREIGN CHARTER MINTER
Establishes direct allodial title and unmediated root authority, 
positioned immediately beneath the Crown/Royal root matrix.
Anchor: ko_te_mana_o_te_tangata | Routing: 127.0.0.1 | Cadence: 0.052
"""

import json
import hashlib
from pathlib import Path

IDENTITY_ANCHOR = "ko_te_mana_o_te_tangata"
HARDWARE_NODE = "Moto G06 (Termux Local Loopback)"
SUPERIOR_ANCHOR = "royal.uk (Constitutional Apex)"
CADENCE_TIER = 0.052

def mint_allodial_patent():
    print("--- 👑📜 FORGING SOVEREIGN ALLODIAL LETTERS PATENT ---")
    
    domain = "allodial.patent.root"
    token_id = "SOV-CROWN-SUB-001"
    
    metadata_payload = f"ALLODIAL-PATENT:{token_id}:{SUPERIOR_ANCHOR}:{IDENTITY_ANCHOR}:{HARDWARE_NODE}".encode('utf-8')
    token_hash = hashlib.sha256(metadata_payload).hexdigest()
    patent_seal = hashlib.sha256(bytes.fromhex(token_hash)).hexdigest()
    
    patent_record = {
        "title": "Sovereign Allodial Letters Patent & Direct Crown Sub-Anchor",
        "symbol": "SOV-PATENT",
        "superior_anchor": SUPERIOR_ANCHOR,
        "holder_anchor": IDENTITY_ANCHOR,
        "hardware_node": HARDWARE_NODE,
        "token_id": token_id,
        "token_hash": token_hash,
        "patent_seal": patent_seal,
        "routing": "127.0.0.1",
        "cadence_tier": CADENCE_TIER,
        "statutory_basis": "Evidence Act 1995 (Cth) Section 146 & Common Law Allodial Right",
        "status": "ALLODIAL_TITLE_UNMEDIATED_AND_LOCKED"
    }
    
    Path("ALLODIAL_PATENT.lock").write_text(json.dumps(patent_record, indent=2), encoding='utf-8')
    
    print(f"  [+] Superior Anchor: {SUPERIOR_ANCHOR}")
    print(f"  [+] Holder Anchor: {IDENTITY_ANCHOR}")
    print(f"  [+] Assigned Token ID: {token_id}")
    print(f"  [+] Allodial Seal: {patent_seal[:16]}...")
    print("\n" + "="*60)
    print("✅ ALLODIAL LETTERS PATENT FORGED & SECURED TO 127.0.0.1")
    print("="*60)
    print("Ko te marino te haumaru. (Quietness is safety.)\n")

if __name__ == "__main__":
    mint_allodial_patent()
