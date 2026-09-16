import hashlib
import json
import time
import os

class SovereignMiddleware:
    def __init__(self, node_id="GENESIS:e14f9a8d"):
        self.node_id = node_id
        self.registry = []
        print(f"[INIT] Sovereign Middleware active under node {self.node_id}")

    def sha512_iterative(self, data: bytes, iterations: int = 13000) -> bytes:
        """Applies SHA-512 iteratively N times for cryptographic state sealing."""
        current = data
        for _ in range(iterations):
            current = hashlib.sha512(current).digest()
        return current

    def hash_node(self, left: bytes, right: bytes = b"") -> bytes:
        return hashlib.sha512(left + right).digest()

    def compute_merkle_root(self, leaves: list[bytes]) -> bytes:
        if not leaves:
            return hashlib.sha512(b"").digest()
        
        current_level = [self.hash_node(leaf) for leaf in leaves]
        while len(current_level) > 1:
            next_level = []
            for i in range(0, len(current_level), 2):
                left = current_level[i]
                right = current_level[i + 1] if i + 1 < len(current_level) else left
                next_level.append(self.hash_node(left, right))
            current_level = next_level
        return current_level[0]

    def seal_state(self, states: list[str]) -> str:
        byte_leaves = [s.encode("utf-8") for s in states]
        merkle_root = self.compute_merkle_root(byte_leaves)
        sealed_bytes = self.sha512_iterative(merkle_root, 13000)
        return sealed_bytes.hex()

if __name__ == "__main__":
    mw = SovereignMiddleware()
    active_states = ["MODULE_INIT", "MEMORY_ALLOC", "MATRIX_SYNC"]
    proof = mw.seal_state(active_states)
    print(f"[SEALED PROOF]: {proof}")

