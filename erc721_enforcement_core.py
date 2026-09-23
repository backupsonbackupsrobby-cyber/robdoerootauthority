# Law of Shaped Force: Strict ERC-721 Identity Enforcement Engine
import sys
import json
import time
import hashlib

LEDGER_FILE = "shaped_force_ledger.json"
# Strict ERC-721 Token Pointer Key Constraint
ENFORCED_TOKEN_ID = "81048664420307000798037101828600347907653676848103297604151295052293545639560"

class ERC721IdentityGuard:
    def __init__(self):
        self.enforced_id = ENFORCED_TOKEN_ID

    def verify_caller_identity(self, providing_id: str) -> bool:
        """Enforces absolute identity matching at the cryptographic perimeter."""
        if providing_id != self.enforced_id:
            print(f"[🚨 SECURITY BREACH] Identity mismatch.")
            print(f" └── Expected: {self.enforced_id[:16]}...")
            print(f" └── Received: {providing_id[:16]}...")
            return False
        return True

    def calculate_enforced_hash(self, block_data: dict) -> str:
        """Computes the strict triple-stage cascade seal over the token state block."""
        serialized = json.dumps(block_data, sort_keys=True).encode('utf-8')
        h1 = hashlib.blake2b(serialized).digest()
        h2 = hashlib.sha3_512(h1).digest()
        return hashlib.sha3_256(h2).hexdigest()

    def strict_commit(self, payload_content: str, token_identity_proof: str):
        """Validates identity parameters stringently before allowing state transitions."""
        print("\n========================================================")
        print("⚡ ENGAGING STRICT ERC-721 IDENTITY CONSTRAINT FILTER ⚡")
        print("========================================================")
        
        # Gate 1: Absolute Identity Verification
        if not self.verify_caller_identity(token_identity_proof):
            print("[CRITICAL] State transition blocked. Access denied.")
            sys.exit(1)
            
        print("[GUARD] Identity authenticated. Querying ledger state...")
        
        # Load active ledger data or bootstrap if empty
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
            "payload": payload_content,
            "previous_hash": prev_hash,
            "identity_auth": self.enforced_id
        }
        
        # Generate identity-sealed hash signature
        new_block["block_hash"] = self.calculate_enforced_hash(new_block)
        ledger.append(new_block)
        
        with open(LEDGER_FILE, 'w') as f:
            json.dump(ledger, f, indent=4)
            
        print(f"[LOCKED] State Block #{new_index} strictly bound to ERC-721 token layer.")
        print(f" └── Block Seal: {new_block['block_hash']}\n")

if __name__ == "__main__":
    import os
    guard = ERC721IdentityGuard()
    
    if len(sys.argv) > 2:
        action_payload = sys.argv[1]
        provided_token = sys.argv[2]
        guard.strict_commit(action_payload, provided_token)
    else:
        print("[MONITOR] Active Guard Standby. Requires: <payload> <token_id>")
