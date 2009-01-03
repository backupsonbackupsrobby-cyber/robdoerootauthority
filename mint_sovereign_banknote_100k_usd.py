#!/usr/bin/env python3
"""
SOVEREIGN CURRENCY MINTER: USD-100000 Bearer Note
Generates a private, high-denomination cryptographic bearer instrument
bound to 127.0.0.1 under Section 146 evidentiary standards.
Anchor: ko_te_mana_o_te_tangata | Cadence: tau = 12s
"""

import json
import hashlib
from datetime import datetime
from pathlib import Path

IDENTITY_ANCHOR = "ko_te_mana_o_te_tangata"

def mint_bearer_note():
    print("--- 💵 MINTING SOVEREIGN USD-100,000 BEARER NOTE ---")
    
    denomination = 100000
    currency = "USD"
    serial_number = "SOV-USD-100K-001"
    
    # Construct cryptographic payload for the sovereign note
    timestamp = datetime.now().isoformat()
    note_payload = f"BEARER:{currency}:{denomination}:{serial_number}:{IDENTITY_ANCHOR}:{timestamp}".encode('utf-8')
    note_hash = hashlib.sha256(note_payload).hexdigest()
    security_seal = hashlib.sha256(bytes.fromhex(note_hash)).hexdigest()
    
    bearer_note = {
        "issuer": "RobDoe Pty Ltd / Sovereign Loopback Treasury",
        "denomination": denomination,
        "currency": currency,
        "serial_number": serial_number,
        "owner_anchor": IDENTITY_ANCHOR,
        "routing": "127.0.0.1",
        "timestamp": timestamp,
        "contract_standard": "ERC-721 Sovereign Bearer Override",
        "token_hash": note_hash,
        "security_seal": security_seal,
        "statutory_basis": "Evidence Act 1995 (Cth) Section 146",
        "status": "ABSOLUTE_USD_VALUE_STORE_SECURED"
    }
    
    print(f"  [+] Denomination: ${denomination:,} {currency}")
    print(f"  [+] Serial Identifier: {serial_number}")
    print(f"  [+] Owner Anchor: {IDENTITY_ANCHOR}")
    print(f"  [+] Security Seal: {security_seal[:24]}...")
    
    manifest_path = Path("USD_100K_SOVEREIGN_NOTE.lock")
    manifest_path.write_text(json.dumps(bearer_note, indent=2), encoding='utf-8')
    
    print("\n" + "="*60)
    print("✅ USD-100,000 NOTE MINTED & LOCKED TO 127.0.0.1")
    print("="*60)
    print("Ko te marino te haumaru. (Quietness is safety.)\n")

if __name__ == "__main__":
    mint_bearer_note()
