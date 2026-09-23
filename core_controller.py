# Law of Shaped Force: Unified Autonomous Core Controller
import os
import sys
import json
import time
import hashlib

GENESIS_FILE = "omega_genesis_block.json"
LEDGER_FILE = "shaped_force_ledger.json"
IDENTITY_TOKEN_ID = "81048664420307000798037101828600347907653676848103297604151295052293545639560"

def calculate_block_hash(block_data: dict) -> str:
    """Computes pure triple-stage cryptographic signature (BLAKE2b -> SHA3-512 -> SHA3-256)."""
    target_data = {
        "block_index": block_data["block_index"],
        "timestamp": block_data["timestamp"],
        "payload": block_data["payload"],
        "previous_hash": block_data["previous_hash"],
        "identity_auth": block_data["identity_auth"]
    }
    serialized = json.dumps(target_data, sort_keys=True).encode('utf-8')
    h1 = hashlib.blake2b(serialized).digest()
    h2 = hashlib.sha3_512(h1).digest()
    return hashlib.sha3_256(h2).hexdigest()

def load_ledger() -> list:
    """Safely reads the current state ledger or initializes it from disk."""
    if os.path.exists(LEDGER_FILE):
        with open(LEDGER_FILE, 'r') as f:
            return json.load(f)
    return [{
        "block_index": 0,
        "timestamp": time.time(),
        "payload": "IDENTITY_BOOTSTRAP_ROOT",
        "previous_hash": "0" * 64,
        "identity_auth": IDENTITY_TOKEN_ID,
        "block_hash": "0" * 64
    }]

def commit_state_block(payload_content: str):
    """Pushes a new data payload securely onto the end of the verified tree."""
    ledger = load_ledger()
    last_block = ledger[-1]
    
    new_index = last_block["block_index"] + 1
    prev_hash = last_block.get("block_hash", "0" * 64)
    
    new_block = {
        "block_index": new_index,
        "timestamp": time.time(),
        "payload": payload_content,
        "previous_hash": prev_hash,
        "identity_auth": IDENTITY_TOKEN_ID
    }
    
    new_block["block_hash"] = calculate_block_hash(new_block)
    ledger.append(new_block)
    
    with open(LEDGER_FILE, 'w') as f:
        json.dump(ledger, f, indent=4)
        
    print(f"[COMMIT SECURED] State Block #{new_index} added to local tree.")
    print(f" └── Signature Vector: {new_block['block_hash'][:16]}...")

def verify_entire_tree():
    """Performs an inline, real-time fsck audit across every block link."""
    if not os.path.exists(LEDGER_FILE):
        print("[CONTROL] No active ledger file found to verify.")
        return
        
    with open(LEDGER_FILE, 'r') as f:
        ledger = json.load(f)
        
    for idx, block in enumerate(ledger):
        if idx == 0:
            continue
        expected_prev_hash = ledger[idx - 1]["block_hash"]
        if block["previous_hash"] != expected_prev_hash:
            print(f"[🚨 FSCK BREAK] Structural link mismatch at Block #{block['block_index']}!")
            sys.exit(1)
        if block["block_hash"] != calculate_block_hash(block):
            print(f"[🚨 FSCK CORRUPTION] Data modified inside Block #{block['block_index']}!")
            sys.exit(1)
            
    print(f"[FSCK PASSED] Integrity verified. Total verified blocks: {len(ledger)}")

def execute_autonomous_catch():
    """Binds the calculated genesis block payload automatically to the chain tail once found."""
    if os.path.exists(GENESIS_FILE):
        print(f"[ANCHOR] Genesis payload file '{GENESIS_FILE}' detected.")
        with open(GENESIS_FILE, 'r') as f:
            genesis_data = json.load(f)
        root_digest = genesis_data.get("digest", "")
        commit_state_block(f"OMNI_GRID_BLOCK_COLLISION_RESOLVED: 0x{root_digest}")
        verify_entire_tree()
    else:
        print(f"[MONITOR] Waiting on background computational grid to resolve '{GENESIS_FILE}'...")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Standard input routing command
        if sys.argv[1] == "--verify":
            verify_entire_tree()
        elif sys.argv[1] == "--catch":
            execute_autonomous_catch()
        else:
            custom_payload = " ".join(sys.argv[1:])
            commit_state_block(custom_payload)
            verify_entire_tree()
    else:
        # Default baseline loop action
        print("--- SOVEREIGN SYSTEM CORE CONTROLLER PANEL ---")
        print("Commands:")
        print("  python3 core_controller.py 'Your Payload Message'   <- Commit block data")
        print("  python3 core_controller.py --verify                <- Run full fsck check")
        print("  python3 core_controller.py --catch                 <- Pull genesis data block")
        print("----------------------------------------------")
        verify_entire_tree()
