# Law of Shaped Force: ISO-Compliant Strict Identity Guard & Event Logger
import sys
import os
import json
import time
import hashlib

LEDGER_FILE = "shaped_force_ledger.json"
COMPLIANCE_LOG = "security_audit_trail.log"
ENFORCED_TOKEN_ID = "81048664420307000798037101828600347907653676848103297604151295052293545639560"

def log_compliance_event(event_type: str, details: str):
    """Writes an immutable, timestamped security event record to disk."""
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    log_entry = f"[{timestamp}] [COMPLIANCE-{event_type}] {details}\n"
    with open(COMPLIANCE_LOG, "a") as f:
        f.write(log_entry)

def calculate_block_hash(block_data: dict) -> str:
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

def execute_compliant_commit(payload: str, provided_token: str):
    print("\n========================================================")
    print("🔎 EVALUATING SECURITY CONTROL CONTROLLER LOGIC 🔎")
    print("========================================================")
    
    if provided_token != ENFORCED_TOKEN_ID:
        error_msg = f"Unauthorized access attempt by token signature: {provided_token[:16]}..."
        print(f"[🚨 SECURITY ALTERATION INTRODUCED] Access Denied.")
        log_compliance_event("BREACH_ATTEMPT_BLOCKED", error_msg)
        sys.exit(1)
        
    log_compliance_event("IDENTITY_AUTHENTICATED", f"Root pointer {ENFORCED_TOKEN_ID[:8]}... cleared write path.")
    
    if os.path.exists(LEDGER_FILE):
        with open(LEDGER_FILE, 'r') as f:
            ledger = json.load(f)
    else:
        ledger = []
        
    new_index = len(ledger)
    prev_hash = ledger[-1]["block_hash"] if new_index > 0 else "0" * 64
    
    new_block = {
        "block_index": new_index,
        "timestamp": time.time(),
        "payload": payload,
        "previous_hash": prev_hash,
        "identity_auth": ENFORCED_TOKEN_ID
    }
    
    new_block["block_hash"] = calculate_block_hash(new_block)
    ledger.append(new_block)
    
    with open(LEDGER_FILE, 'w') as f:
        json.dump(ledger, f, indent=4)
        
    log_compliance_event("BLOCK_ANCHORED", f"Block #{new_index} locked with hash {new_block['block_hash'][:16]}...")
    print(f"[SUCCESS] Compliance Block #{new_index} successfully committed to ledger architecture.")

if __name__ == "__main__":
    if len(sys.argv) > 2:
        execute_compliant_commit(sys.argv[1], sys.argv[2])
    else:
        print("[POSTURE] Active Standby. Compliance engine awaiting structured parameters.")
