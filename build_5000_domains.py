import hashlib
import json
import time

def generate_domain_chest(chest_id=1, count=5000, base_tld="atom"):
    print(f"[*] Generating {count} Domain Records for Chest #{chest_id}...")
    
    domain_records = []
    leaves = []
    
    timestamp = int(time.time())
    
    for i in range(count):
        domain_name = f"node-{i:04d}.{base_tld}"
        # Compute ENS-style label hash
        label_hash = hashlib.sha256(domain_name.encode('utf-8')).hexdigest()
        
        record = {
            "index": i,
            "domain": domain_name,
            "label_hash": f"0x{label_hash}",
            "chest_id": chest_id
        }
        domain_records.append(record)
        
        # Build Merkle Leaf: Hash(index + domain + label_hash)
        leaf_raw = f"{i}:{domain_name}:{label_hash}".encode('utf-8')
        leaf_hash = hashlib.sha256(leaf_raw).hexdigest()
        leaves.append(leaf_hash)

    # Compute Merkle Root
    tree = leaves
    while len(tree) > 1:
        if len(tree) % 2 != 0:
            tree.append(tree[-1])
        tree = [
            hashlib.sha256((tree[j] + tree[j+1]).encode('utf-8')).hexdigest()
            for j in range(0, len(tree), 2)
        ]
        
    merkle_root = tree[0]
    
    manifest = {
        "chest_id": chest_id,
        "total_domains": count,
        "base_tld": base_tld,
        "timestamp": timestamp,
        "domain_merkle_root": merkle_root,
        "domains_sample": domain_records[:5] # Sample first 5
    }
    
    with open("5000_domain_manifest.json", "w") as f:
        json.dump(manifest, f, indent=2)
        
    print("==================================================")
    print("   5,000 DOMAIN BUNDLE MANIFEST COMPLETE")
    print("==================================================")
    print(f"[+] Total Domains : {count}")
    print(f"[+] TLD Scope     : .{base_tld}")
    print(f"[+] Merkle Root   : 0x{merkle_root}")
    print(f"[+] Sample Range  : {domain_records[0]['domain']} -> {domain_records[-1]['domain']}")
    print("[+] Saved manifest to: ~/robdoerootauthority/5000_domain_manifest.json")

if __name__ == "__main__":
    generate_domain_chest()
