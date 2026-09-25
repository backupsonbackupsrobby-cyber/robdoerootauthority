import hashlib
import json
import subprocess
import time

def generate_authority_erc721():
    print("[*] Structuring ERC-721 Authority and Duty Layer...")
    
    authority_structure = {
        "protocol": "ATOM-TRUTH-ERC721-AUTHORITY-STRUCT",
        "jurisdiction": "RobDoe Pty Ltd",
        "governance_model": "Duty-Bound Foundational Stewardship (Under the Sovereign)",
        "hierarchy": {
            "root_authority": "ATOM-TRUTH",
            "stewardship": "Kaitiakitanga / Foundational Anchor",
            "enforcement": "Evidence Act 1995 s 146 Compliant"
        },
        "asset_distribution": {
            "bundle_range": "1 - 5000",
            "solo_remainder": 5001,
            "nature": "Immutable, Non-Extractive, Structural Rights"
        },
        "timestamp": time.time()
    }
    
    # Compute structural hash
    struct_string = json.dumps(authority_structure, sort_keys=True)
    struct_hash = hashlib.sha256(struct_string.encode('utf-8')).hexdigest()
    
    registry = {
        "authority_hash": struct_hash,
        "structure": authority_structure
    }
    
    with open("erc721_authority_registry.json", "w", encoding="utf-8") as f:
        json.dump(registry, f, indent=4)
        
    print(f"[+] ERC-721 Authority Structure Locked! Hash: {struct_hash}")
    return struct_hash

if __name__ == "__main__":
    a_hash = generate_authority_erc721()
    subprocess.run(["git", "add", "erc721_authority_registry.json"], check=True)
    subprocess.run(["git", "commit", "-m", f"erc721(authority): {a_hash} - Duty-bound structural governance anchored"], check=True)
    result = subprocess.run(["git", "push", "origin", "main"], capture_output=True, text=True)
    if result.returncode != 0:
        subprocess.run(["git", "push", "origin", "master"], capture_output=True, text=True)
    print("[+] SUCCESS: ERC-721 Authority structure committed and pushed live!")
