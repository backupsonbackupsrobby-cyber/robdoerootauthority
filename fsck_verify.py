# Law of Shaped Force: Zero-Dependency Ledger FSCK Integrity Scanner
import json
import os
import sys
import hashlib

LEDGER_FILE = "shaped_force_ledger.json"

def calculate_block_hash(block_data: dict) -> str:
    """Recalculates the multi-vector hash matrix signature for verification."""
    # Copy block parameters except the signature hash itself to rebuild the original matrix
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

def verify_ledger_integrity():
    print("========================================================")
    print("🔎 RUNNING CRYPTOGRAPHIC MERKLE FSCK INTEGRITY SCAN 🔎")
    print("========================================================")
    
    if not os.path.exists(LEDGER_FILE):
        print(f"[ERR] Scan aborted: Target file '{LEDGER_FILE}' does not exist.")
        sys.exit(1)
        
    with open(LEDGER_FILE, 'r') as f:
        ledger = json.load(f)
        
    print(f"[STATUS] Analyzing {len(ledger)} sequential blocks in active memory...")
    
    for idx, block in enumerate(ledger):
        # Skip checking structural zero links on the original bootstrap node #0
        if idx == 0:
            if block["block_hash"] != "0" * 64:
                print(f"[🚨 FAILURE] Block #0 signature format corrupted.")
                sys.exit(1)
            continue
            
        expected_prev_hash = ledger[idx - 1]["block_hash"]
        
        # 1. Verify Parent-Child Structural Chaining Link
        if block["previous_hash"] != expected_prev_hash:
            print(f"[🚨 STRUCTURAL BREAK AT BLOCK #{block['block_index']}]")
            print(f" └── Expected Previous Hash: {expected_prev_hash[:16]}...")
            print(f" └── Found Corrupted Hash:   {block['previous_hash'][:16]}...")
            sys.exit(1)
            
        # 2. Recompute and Verify Mathematical Content Integrity Seal
        computed_seal = calculate_block_hash(block)
        if block["block_hash"] != computed_seal:
            print(f"[🚨 DATA MODIFICATION DETECTED AT BLOCK #{block['block_index']}]")
            print(f" └── Ledger Hash:   {block['block_hash'][:16]}...")
            print(f" └── Computed Hash: {computed_seal[:16]}...")
            sys.exit(1)
            
        print(f" ├── [VERIFIED] Block #{block['block_index']} link sealed. Hash: {computed_seal[:12]}...")

    print("========================================================")
    print("✅ FSCK SUCCESS: Cryptographic chain layout untampered.")
    print("========================================================")

if __name__ == "__main__":
    verify_ledger_integrity()
