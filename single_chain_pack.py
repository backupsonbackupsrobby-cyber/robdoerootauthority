import json
import hashlib

def create_single_chain_payload(count=5000, base_tld="atom"):
    print(f"[*] Packing {count} domains into a single on-chain payload...")
    
    domains = [f"node-{i:04d}.{base_tld}" for i in range(count)]
    
    # 1. Bytecode Blob (Concatenated for SSTORE2 / On-chain storage)
    raw_payload = ",".join(domains).encode('utf-8')
    hex_payload = raw_payload.hex()
    
    # 2. Merkle Root Hash
    leaves = [hashlib.sha256(d.encode('utf-8')).hexdigest() for d in domains]
    tree = leaves
    while len(tree) > 1:
        if len(tree) % 2 != 0:
            tree.append(tree[-1])
        tree = [
            hashlib.sha256((tree[i] + tree[i+1]).encode('utf-8')).hexdigest()
            for i in range(0, len(tree), 2)
        ]
    
    merkle_root = tree[0]
    
    output = {
        "total_domains": count,
        "payload_bytes_len": len(raw_payload),
        "merkle_root": f"0x{merkle_root}",
        "hex_bytecode_preview": f"0x{hex_payload[:64]}..."
    }
    
    with open("single_chain_bundle.json", "w") as f:
        json.dump(output, f, indent=2)
        
    print("==================================================")
    print("   SINGLE ON-CHAIN BUNDLE READY")
    print("==================================================")
    print(f"[+] Total Domains    : {count}")
    print(f"[+] On-Chain Raw Size: {len(raw_payload)} bytes (~{len(raw_payload)/1024:.2f} KB)")
    print(f"[+] Single State Slot: 0x{merkle_root}")
    print("==================================================")

if __name__ == "__main__":
    create_single_chain_payload()
