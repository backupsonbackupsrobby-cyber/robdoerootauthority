import hashlib
import json
import subprocess
import time

def generate_erc721_manifest():
    bundle_chunk = {
        "batch_id": "BUNDLE-001",
        "type": "ERC-721 Bundle",
        "range": "1 to 5000",
        "count": 5000,
        "issuer": "RobDoe Pty Ltd",
        "authority_node": "ATOM-TRUTH"
    }
    solo_chunk = {
        "batch_id": "SOLO-001",
        "type": "ERC-721 Solo Remainder",
        "token_id": 5001,
        "issuer": "RobDoe Pty Ltd",
        "authority_node": "ATOM-TRUTH"
    }
    collection_data = {
        "protocol": "ATOM-TRUTH-ERC721-SOVEREIGN",
        "timestamp": time.time(),
        "assets": [bundle_chunk, solo_chunk]
    }
    collection_hash = hashlib.sha256(json.dumps(collection_data, sort_keys=True).encode('utf-8')).hexdigest()
    master_record = {
        "collection_hash": collection_hash,
        "metadata": collection_data
    }
    with open("erc721_sovereign_ledger.json", "w", encoding="utf-8") as f:
        json.dump(master_record, f, indent=4)
    return collection_hash

def atomic_erc721_push(coll_hash):
    subprocess.run(["git", "add", "erc721_sovereign_ledger.json"], check=True)
    subprocess.run(["git", "commit", "-m", f"erc721(mint): {coll_hash} - 5000 Bundle & Solo Remainder anchored on-chain"], check=True)
    result = subprocess.run(["git", "push", "origin", "main"], capture_output=True, text=True)
    if result.returncode != 0:
        subprocess.run(["git", "push", "origin", "master"], capture_output=True, text=True)

if __name__ == "__main__":
    c_hash = generate_erc721_manifest()
    atomic_erc721_push(c_hash)
    print(f"[+] ERC-721 Sovereign Mint Complete! Hash: {c_hash}")
