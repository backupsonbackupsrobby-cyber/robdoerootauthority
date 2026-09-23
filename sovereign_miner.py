import hashlib
import json
import time

class SovereignBlock:
    def __init__(self, index, previous_hash, assets, nonce=0):
        self.index = index
        self.timestamp = time.time()
        self.previous_hash = previous_hash
        self.assets = assets
        self.nonce = nonce
        self.hash = self.compute_hash()

    def compute_hash(self):
        block_string = json.dumps({
            "index": self.index,
            "timestamp": self.timestamp,
            "previous_hash": self.previous_hash,
            "assets": self.assets,
            "nonce": self.nonce
        }, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()

    def mine(self, difficulty=3):
        target = "0" * difficulty
        print(f"[*] Mining Block #{self.index} for target '{target}'...")
        while not self.hash.startswith(target):
            self.nonce += 1
            self.hash = self.compute_hash()
        print(f"[+] Block #{self.index} Mined! Hash: {self.hash} (Nonce: {self.nonce})")

class SovereignChain:
    def __init__(self):
        self.chain = []
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_block = SovereignBlock(0, "0", {"authority": "ATOM-TRUTH | RobDoe Pty Ltd", "asset": "Genesis Anchor"})
        genesis_block.mine(difficulty=2)
        self.chain.append(genesis_block)

    def add_block(self, assets, difficulty=3):
        previous_block = self.chain[-1]
        new_block = SovereignBlock(len(self.chain), previous_block.hash, assets)
        new_block.mine(difficulty)
        self.chain.append(new_block)

if __name__ == "__main__":
    print("[*] Initializing ATOM-TRUTH Sovereign Chain & Asset Ledger...")
    chain = SovereignChain()

    print("\n[*] Minting Chunk 1: 5,000 Bundle Assets...")
    chain.add_block({"chunk": 1, "type": "ERC-721 Bundle", "count": 5000, "entity": "RobDoe Pty Ltd"}, difficulty=3)

    print("\n[*] Minting Chunk 2: Solo Remainder Assets...")
    chain.add_block({"chunk": 2, "type": "ERC-721 Solo Remainder", "count": 1, "entity": "RobDoe Pty Ltd"}, difficulty=3)

    print("\n==================================================")
    print("   EMPIRE SUCCESSFULLY MINED & ANCHORED ON-CHAIN")
    print("==================================================")
    for block in chain.chain:
        print(f"Block {block.index} [Hash: {block.hash[:16]}... | Nonce: {block.nonce}]")
