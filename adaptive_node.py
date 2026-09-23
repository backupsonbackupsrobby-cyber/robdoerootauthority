# Law of Shaped Force: Autonomous Adaptive Feedback Node
import time
import socket
import sys
import hashlib
import subprocess
import os
import json

HOST = '127.0.0.1'
PORT = 8888

class AntifragileEngine:
    def __init__(self):
        self.registry = {}
        self.next_token_id = 1
        self.total_perturbations = 0
        self.security_entropy_pool = hashlib.sha256(b"GENESIS").hexdigest()

    def digest_friction(self, fault_type, raw_context):
        self.total_perturbations += 1
        seed = f"{self.security_entropy_pool}-{fault_type}-{raw_context}"
        self.security_entropy_pool = hashlib.sha256(seed.encode('utf-8')).hexdigest()
        print(f"[ABSORBED] Resistance Cycles: {self.total_perturbations}")

    def mint(self, owner_addr, metadata):
        token_id = self.next_token_id
        metadata["entropy_proof"] = self.security_entropy_pool
        metadata["address_608"] = owner_addr
        self.registry[token_id] = {"owner": owner_addr, "metadata": metadata}
        self.next_token_id += 1
        print(f"[MINT] Token ID {token_id} assigned to address {owner_addr}")
        return token_id

    def compute_merkle_root(self):
        # Convert registry state into cryptographic leaves
        leaves = [hashlib.sha3_256(json.dumps(node, sort_keys=True).encode('utf-8')).digest() for node in self.registry.values()]
        if not leaves:
            leaves = [hashlib.sha3_256(b"AGGRESSIVE_TRUTH_GENESIS").digest()]
        
        def build_root(nodes):
            if len(nodes) == 1:
                return nodes[0]
            next_level = []
            for i in range(0, len(nodes), 2):
                left = nodes[i]
                right = nodes[i+1] if i + 1 < len(nodes) else left
                next_level.append(hashlib.sha3_256(left + right).digest())
            return build_root(next_level)
        
        return build_root(leaves).hex()

    def anchor_state(self):
        root_hex = self.compute_merkle_root()
        tag_name = f"merkle-root-{root_hex[:12]}"
        print(f"[AGGRESSIVE TRUTH] Local Root Hash: 0x{root_hex}")
        
        if not os.path.exists(".git"):
            subprocess.run(["git", "init"], capture_output=True)
            subprocess.run(["git", "config", "user.name", "RobDoe"], capture_output=True)
            subprocess.run(["git", "config", "user.email", "robdoe@local.authority"], capture_output=True)

        existing = subprocess.run(["git", "tag"], capture_output=True, text=True).stdout.splitlines()
        if tag_name not in existing:
            subprocess.run(["git", "add", "."], capture_output=True)
            subprocess.run(["git", "commit", "-m", f"Aggressive state anchor: {root_hex[:12]}"], capture_output=True)
            subprocess.run(["git", "tag", "-a", tag_name, "-m", f"Root: 0x{root_hex}"], capture_output=True)
            print(f"[ANCHOR SUCCESS] State locked to Git tag: {tag_name}")
        else:
            print(f"[VERIFIED] State root {tag_name} already anchored.")

if __name__ == "__main__":
    print("[DAEMON] Initializing Antifragile Engine...")
    engine = AntifragileEngine()
    
    # Digest external ICANN/DNS noise as raw friction
    engine.digest_friction("icann_noise", "bypassed_legacy_dns")
    
    # Mint sovereign state with the 608 metadata address
    engine.mint("608", {"domain": "robdoe.crypto", "state": "sovereign"})
    
    # Compute Merkle root and anchor to Git
    engine.anchor_state()
