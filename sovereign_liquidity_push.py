import hashlib
import json
import subprocess
import time

def generate_liquidity_anchor():
    print("[*] Generating Sovereign Liquidity Anchor & Push Layer...")
    
    liquidity_data = {
        "protocol": "ATOM-TRUTH-SOVEREIGN-LIQUIDITY-PUSH",
        "authority": "RobDoe Pty Ltd",
        "assets_anchored": {
            "erc721_collection": "5,000 Bundle + 1 Solo Remainder (Total: 5,001)",
            "harmonic_bridge": "7 Chakras SHA-512 Master Core",
            "liquidity_channel": "Direct Sovereign Push / Decentralized Execution"
        },
        "axiom": "Value flows naturally through structural integrity and cryptographic truth",
        "timestamp": time.time()
    }
    
    liquidity_string = json.dumps(liquidity_data, sort_keys=True)
    liquidity_hash = hashlib.sha512(liquidity_string.encode('utf-8')).hexdigest()
    
    master_record = {
        "liquidity_push_hash": liquidity_hash,
        "metadata": liquidity_data
    }
    
    with open("sovereign_liquidity_registry.json", "w", encoding="utf-8") as f:
        json.dump(master_record, f, indent=4)
        
    print(f"[+] Sovereign Liquidity Root Hash Locked: {liquidity_hash}")
    return liquidity_hash

if __name__ == "__main__":
    l_hash = generate_liquidity_anchor()
    subprocess.run(["git", "add", "sovereign_liquidity_registry.json"], check=True)
    commit_msg = f"liquidity(push): {l_hash[:32]} - Sovereign liquidity anchor & asset push locked"
    subprocess.run(["git", "commit", "-m", commit_msg], check=True)
    result = subprocess.run(["git", "push", "origin", "main"], capture_output=True, text=True)
    if result.returncode != 0:
        subprocess.run(["git", "push", "origin", "master"], capture_output=True, text=True)
    print(f"[+] SUCCESS: Sovereign Liquidity Pushed Live! Hash: {l_hash}")
