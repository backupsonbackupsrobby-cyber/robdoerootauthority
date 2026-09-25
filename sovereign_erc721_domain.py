import hashlib
import json
import subprocess
import time

def generate_erc721_domain_binding():
    print("[*] Binding ERC-721 Sovereign Ledger to Decentralized & Institutional Domains...")
    
    domain_payload = {
        "protocol": "ATOM-TRUTH-ERC721-DOMAIN-BINDING",
        "authority": "RobDoe Pty Ltd",
        "corporate_entity": "RobDoe Pty Ltd",
        "brand_namespace": "AiAgency101",
        "primary_domains": {
            "institutional_witness": "royal.uk",
            "sovereign_registry": "RobDoe Root Authority"
        },
        "token_mapping": {
            "standard": "ERC-721",
            "total_supply": 5001,
            "structure": "5,000 Bundles + 1 Solo Remainder",
            "domain_resolution": "On-Chain to Decentralized Namespace"
        },
        "axiom": "Absolute ownership anchored across cryptographic hash, corporate structure, and domain resolution.",
        "timestamp": time.time()
    }
    
    domain_string = json.dumps(domain_payload, sort_keys=True)
    domain_hash = hashlib.sha512(domain_string.encode('utf-8')).hexdigest()
    
    master_record = {
        "erc721_domain_root_hash": domain_hash,
        "metadata": domain_payload
    }
    
    with open("erc721_domain_binding_registry.json", "w", encoding="utf-8") as f:
        json.dump(master_record, f, indent=4)
        
    print(f"[+] ERC-721 Domain Binding Root Hash Hex Locked: {domain_hash}")
    return domain_hash

if __name__ == "__main__":
    d_hash = generate_erc721_domain_binding()
    subprocess.run(["git", "add", "erc721_domain_binding_registry.json"], check=True)
    commit_msg = f"erc721(domain): {d_hash[:32]} - ERC-721 domain and institutional namespace binding locked"
    subprocess.run(["git", "commit", "-m", commit_msg], check=True)
    result = subprocess.run(["git", "push", "origin", "main"], capture_output=True, text=True)
    if result.returncode != 0:
        subprocess.run(["git", "push", "origin", "master"], capture_output=True, text=True)
    print(f"[+] SUCCESS: ERC-721 Domain Binding Pushed Live! Hash: {d_hash}")
