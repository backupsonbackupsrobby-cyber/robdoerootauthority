# Law of Shaped Force: Sovereign Identity Binder
import os
import sys
import json
import time
import hashlib

GENESIS_FILE = "omega_genesis_block.json"
LEDGER_FILE = "shaped_force_ledger.json"
IDENTITY_TOKEN_ID = "81048664420307000798037101828600347907653676848103297604151295052293545639560"

def calculate_block_hash(block_data: dict) -> str:
    serialized = json.dumps(block_data, sort_keys=True).encode('utf-8')
    h1 = hashlib.blake2b(serialized).digest()
    h2 = hashlib.sha3_512(h1).digest()
    return hashlib.sha3_256(h2).hexdigest()

def append_identity_signed_state(payload_content: str):
    # Check if ledger already exists, if not, create standard track template
    if os.path.exists(LEDGER_FILE):
        with open(LEDGER_FILE, 'r') as f:
            ledger = json.load(f)
    else:
        # Standalone initialization placeholder if genesis is still processing
        ledger = [{
            "block_index": 0,
            "timestamp": time.time(),
            "payload": "IDENTITY_BOOTSTRAP_ROOT",
            "previous_hash": "0" * 64,
            "identity_auth": IDENTITY_TOKEN_ID,
            "block_hash": "0" * 64
        }]
        
    last_block = ledger[-1]
    new_index = last_block["block_index"] + 1
    prev_hash = last_block.get("block_hash", "0" * 64)
    
    new_block = {
        "block_index": new_index,
        "timestamp": time.time(),
        "payload": payload_content,
        "previous_hash": prev_hash,
        "identity_auth": IDENTITY_TOKEN_ID  # Automatically sign under your ERC-721 pointer
    }
    
    new_block["block_hash"] = calculate_block_hash(new_block)
    ledger.append(new_block)
    
    with open(LEDGER_FILE, 'w') as f:
        json.dump(ledger, f, indent=4)
        
    print(f"[SIGNED & LOCKED] State Block #{new_index} anchored to Identity Token ID.")
    print(f" └── Signature Vector: {new_block['block_hash'][:16]}...")

if __name__ == "__main__":
    payload = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "STATE_TRANSITION: INITIAL_SECURE_HEARTBEAT"
    append_identity_signed_state(payload)
