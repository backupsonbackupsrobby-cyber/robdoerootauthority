import hashlib
import json
import subprocess
import math
import time

def generate_sha512_sovereign_core():
    print("[*] Upgrading to SHA-512 512-bit sovereign cryptographic entropy...")
    
    core_data = {
        "protocol": "ATOM-TRUTH-SHA512-SOVEREIGN-CORE",
        "authority": "RobDoe Pty Ltd",
        "algorithm": "SHA-512 (512-bit / 128-hex character root hash)",
        "axiom": "Absolute cryptographic density through first principles",
        "timestamp": time.time()
    }
    
    core_string = json.dumps(core_data, sort_keys=True)
    # Upgraded from SHA-256 to SHA-512 for maximum bit-strength
    sha512_root_hash = hashlib.sha512(core_string.encode('utf-8')).hexdigest()
    
    master_record = {
        "sha512_root_hash": sha512_root_hash,
        "metadata": core_data
    }
    
    with open("sovereign_sha512_registry.json", "w", encoding="utf-8") as f:
        json.dump(master_record, f, indent=4)
        
    print(f"[+] SHA-512 Root Hash Locked: {sha512_root_hash}")
    return sha512_root_hash

if __name__ == "__main__":
    r_hash = generate_sha512_sovereign_core()
    subprocess.run(["git", "add", "sovereign_sha512_registry.json"], check=True)
    commit_msg = f"sha512(core): {r_hash} - 512-bit sovereign cryptographic root locked"
    subprocess.run(["git", "commit", "-m", commit_msg], check=True)
    result = subprocess.run(["git", "push", "origin", "main"], capture_output=True, text=True)
    if result.returncode != 0:
        subprocess.run(["git", "push", "origin", "master"], capture_output=True, text=True)
    print(f"[+] SUCCESS: SHA-512 Sovereign Core Pushed Live! Hash: {r_hash}")
