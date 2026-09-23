# Law of Shaped Force: Zero-Dependency Merkle State Chainer
import os
import sys
import json
import time
import hashlib

GENESIS_FILE = "omega_genesis_block.json"
LEDGER_FILE = "shaped_force_ledger.json"

def calculate_block_hash(block_data: dict) -> str:
    """Computes a strict multi-vector signature of a ledger block."""
    serialized = json.dumps(block_data, sort_keys=True).encode('utf-8')
    h1 = hashlib.blake2b(serialized).digest()
    h2 = hashlib.sha3_512(h1).digest()
    return hashlib.sha3_256(h2).hexdigest()

def initialize_ledger() -> list:
    """Safely loads or bootstraps the ledger structure from the genesis manifest."""
    if not os.path.exists(GENESIS_FILE):
        print(f"[WAITING] Genesis root '{GENESIS_FILE}' not found yet. Tree is still resolving...")
        sys.exit(0)
        
    if os.path.exists(LEDGER_FILE):
        with open(LEDGER_FILE, 'r') as f:
            return json.load(f)
            
    # Bootstrap ledger using the autonomous grid's genesis block
    with open(GENESIS_FILE, 'r') as f:
        genesis_data = json.load(f)
        
    genesis_hash = genesis_data.get("digest")
    print(f"[BOOTSTRAP] Merkle root detected: {genesis_hash[:16]}...")
    
    genesis_block = {
        "block_index": 0,
        "timestamp": genesis_data.get("timestamp", time.time()),
        "payload": genesis_data.get("payload", "GENESIS_ROOT"),
        "previous_hash": "0" * 64,
        "block_hash": genesis_hash
    }
    
    ledger = [genesis_block]
    with open(LEDGER_FILE, 'w') as f:
        json.dump(ledger, f, indent=4)
    print(f"[INITIALIZED] Immutable ledger started at {LEDGER_FILE}")
    return ledger

def append_state_block(payload_content: str):
    """Chains a new cryptographic state block onto the tip of the Merkle tree."""
    ledger = initialize_ledger()
    last_block = ledger[-1]
    
    new_index = last_block["block_index"] + 1
    prev_hash = last_block["block_hash"]
    
    new_block_template = {
        "block_index": new_index,
        "timestamp": time.time(),
        "payload": payload_content,
        "previous_hash": prev_hash
    }
    
    # Secure the new block hash
    new_block_template["block_hash"] = calculate_block_hash(new_block_template)
    
    ledger.append(new_block_template)
    with open(LEDGER_FILE, 'w') as f:
        json.dump(ledger, f, indent=4)
        
    print(f"[SECURED] Block #{new_index} added to tree.")
    print(f" └── Prev Hash: {prev_hash[:16]}...")
    print(f" └── Curr Hash: {new_block_template['block_hash'][:16]}...")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        # Defaults to a health check if no payload argument is provided
        initialize_ledger()
    else:
        user_payload = " ".join(sys.argv[1:])
        append_state_block(user_payload)
