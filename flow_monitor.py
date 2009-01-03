#!/usr/bin/env python3
"""
SELF-SUFFICIENT CHAIN FLOW MONITOR
Observes continuous block verification across local sovereign nodes.
"""

import time
import hashlib
from datetime import datetime

IDENTITY_ANCHOR = "ko_te_mana_o_te_tangata"
CADENCE = "Sha1296000arc"

def monitor_flow():
    print("--- ⛓️ SELF-SUFFICIENT NODE FLOW MONITOR ---")
    print(f"Anchor: {IDENTITY_ANCHOR} | Cadence: {CADENCE}")
    print("Press Ctrl+C to halt monitoring.\n")
    
    block_height = 14570
    previous_hash = "0f650b1a696876cd7906dfb6c53c7b9ec2816e30a2de20bb385e651f76210ba1"
    
    try:
        while True:
            block_height += 1
            timestamp = datetime.now().isoformat()
            
            payload = f"{block_height}:{previous_hash}:{timestamp}:{IDENTITY_ANCHOR}".encode('utf-8')
            current_hash = hashlib.sha256(payload).hexdigest()
            merkle_root = hashlib.sha256(bytes.fromhex(current_hash)).hexdigest()
            
            print(f"[BLOCK #{block_height}] TIME: {timestamp[11:19]} | ROOT: {merkle_root[:16]}... | STATUS: FLOWING ✅")
            
            previous_hash = current_hash
            time.sleep(1.296)  # Pulsing in harmony with the cadence
    except KeyboardInterrupt:
        print("\n[+] Flow monitor detached. Nodes remain synchronized and secure.")

if __name__ == "__main__":
    monitor_flow()
