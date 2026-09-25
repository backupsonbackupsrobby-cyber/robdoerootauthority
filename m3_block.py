import hashlib
import json
import time

def build_m3_block(chest_id=1, total_assets=5000):
    print(f"[*] Initializing BLOCK M3 Execution...")
    timestamp = int(time.time())
    
    # Generate 5,000 Asset Leaf Array
    leaves = []
    for idx in range(total_assets):
        raw_leaf = f"M3:CHEST:{chest_id}:ASSET:{idx}:{timestamp}".encode('utf-8')
        leaf_hash = hashlib.sha256(raw_leaf).hexdigest()
        leaves.append(leaf_hash)
    
    # Compute Merkle Root for Block M3
    tree = leaves
    while len(tree) > 1:
        if len(tree) % 2 != 0:
            tree.append(tree[-1])
        tree = [
            hashlib.sha256((tree[i] + tree[i+1]).encode('utf-8')).hexdigest()
            for i in range(0, len(tree), 2)
        ]
    
    m3_merkle_root = tree[0]
    
    # Block M3 Header
    m3_block_header = {
        "block": "M3",
        "chest_id": chest_id,
        "capacity": total_assets,
        "timestamp": timestamp,
        "genesis_ref": "e14f9a8d",
        "tag_ref": "v14.0.0-erc721-mainnet-root-20260923-134439",
        "m3_merkle_root": m3_merkle_root
    }
    
    # Compute Final Block M3 Hash Seal
    header_bytes = json.dumps(m3_block_header, sort_keys=True).encode('utf-8')
    m3_seal_hash = hashlib.sha512(header_bytes).hexdigest()
    
    print("==================================================")
    print("   TERMUX BLOCK M3 SEAL COMPLETE")
    print("==================================================")
    print(f"[+] Block ID       : M3")
    print(f"[+] Total Assets   : {total_assets}")
    print(f"[+] Merkle Root    : {m3_merkle_root}")
    print(f"[+] M3 Seal (512)  : {m3_seal_hash[:64]}...")
    print("==================================================")

    # Save to workspace manifest
    with open("m3_block_manifest.json", "w") as f:
        json.dump(m3_block_header, f, indent=2)
    print("[+] Saved manifest to: ~/robdoerootauthority/m3_block_manifest.json")

if __name__ == "__main__":
    build_m3_block()
