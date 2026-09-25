import hashlib
import json
import subprocess
import time

def generate_pound_mint():
    print("[*] Minting Sovereign Pound (GBP / Sterling Anchor) layer...")
    
    pound_mint_data = {
        "protocol": "ATOM-TRUTH-POUND-MINT",
        "issuer": "RobDoe Pty Ltd",
        "authority_node": "ATOM-TRUTH",
        "asset_class": "Sovereign Pound Sterling Anchor",
        "backing": "Ground-Up Structural Duty & Merkle Integrity",
        "timestamp": time.time()
    }
    
    pound_string = json.dumps(pound_mint_data, sort_keys=True)
    pound_hash = hashlib.sha256(pound_string.encode('utf-8')).hexdigest()
    
    master_record = {
        "pound_mint_hash": pound_hash,
        "metadata": pound_mint_data
    }
    
    with open("pound_sovereign_mint.json", "w", encoding="utf-8") as f:
        json.dump(master_record, f, indent=4)
        
    print(f"[+] Pound Sovereign Mint Locked! Hash: {pound_hash}")
    return pound_hash

if __name__ == "__main__":
    p_hash = generate_pound_mint()
    subprocess.run(["git", "add", "pound_sovereign_mint.json"], check=True)
    subprocess.run(["git", "commit", "-m", f"pound(mint): {p_hash} - Sovereign Pound sterling anchor locked"], check=True)
    result = subprocess.run(["git", "push", "origin", "main"], capture_output=True, text=True)
    if result.returncode != 0:
        subprocess.run(["git", "push", "origin", "master"], capture_output=True, text=True)
    print(f"[+] SUCCESS: Sovereign Pound Mint Complete! Hash: {p_hash}")
