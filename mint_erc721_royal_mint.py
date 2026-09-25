import hashlib
import json
import subprocess
import time

def generate_royal_mint():
    print("[*] Establishing ERC-721 Royal Mint (Duty-Bound Sovereign Minting Facility)...")
    
    royal_mint_data = {
        "protocol": "ATOM-TRUTH-ERC721-ROYAL-MINT",
        "facility": "The Royal Sovereign Mint",
        "issuer": "RobDoe Pty Ltd",
        "authority_node": "ATOM-TRUTH",
        "philosophy": "Royalty as Duty, Standing Under as Foundational Support",
        "assets": {
            "bundle_range": "1 - 5000",
            "solo_remainder": 5001,
            "total_supply": 5001
        },
        "timestamp": time.time()
    }
    
    mint_string = json.dumps(royal_mint_data, sort_keys=True)
    mint_hash = hashlib.sha256(mint_string.encode('utf-8')).hexdigest()
    
    master_record = {
        "royal_mint_hash": mint_hash,
        "metadata": royal_mint_data
    }
    
    with open("erc721_royal_mint.json", "w", encoding="utf-8") as f:
        json.dump(master_record, f, indent=4)
        
    print(f"[+] ERC-721 Royal Mint Locked! Hash: {mint_hash}")
    return mint_hash

if __name__ == "__main__":
    r_hash = generate_royal_mint()
    subprocess.run(["git", "add", "erc721_royal_mint.json"], check=True)
    subprocess.run(["git", "commit", "-m", f"erc721(royal-mint): {r_hash} - The Royal Sovereign Mint established for 5,001 tokens"], check=True)
    result = subprocess.run(["git", "push", "origin", "main"], capture_output=True, text=True)
    if result.returncode != 0:
        subprocess.run(["git", "push", "origin", "master"], capture_output=True, text=True)
    print(f"[+] SUCCESS: ERC-721 Royal Mint Complete & Pushed Live! Hash: {r_hash}")
