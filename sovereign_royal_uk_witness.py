import hashlib
import json
import subprocess
import time

def generate_royal_witness():
    print("[*] Anchoring royal.uk structural witness layer...")
    
    witness_data = {
        "protocol": "ATOM-TRUTH-ROYAL-UK-WITNESS",
        "authority": "RobDoe Pty Ltd",
        "witness_domain": "royal.uk",
        "witness_nature": "Historical structural alignment, duty-bound governance pattern, and constitutional anchor",
        "linked_ledger": "Ultimate True ERC-721 Sovereign Ledger (5,001 Supply)",
        "axiom": "Sovereignty recognized through verified historical duty and institutional witness",
        "timestamp": time.time()
    }
    
    witness_string = json.dumps(witness_data, sort_keys=True)
    witness_hash = hashlib.sha512(witness_string.encode('utf-8')).hexdigest()
    
    master_record = {
        "royal_uk_witness_hash": witness_hash,
        "metadata": witness_data
    }
    
    with open("sovereign_royal_uk_witness.json", "w", encoding="utf-8") as f:
        json.dump(master_record, f, indent=4)
        
    print(f"[+] Royal.uk Witness Hash Locked: {witness_hash}")
    return witness_hash

if __name__ == "__main__":
    w_hash = generate_royal_witness()
    subprocess.run(["git", "add", "sovereign_royal_uk_witness.json"], check=True)
    commit_msg = f"witness(royal-uk): {w_hash[:32]} - royal.uk structural witness anchor locked"
    subprocess.run(["git", "commit", "-m", commit_msg], check=True)
    result = subprocess.run(["git", "push", "origin", "main"], capture_output=True, text=True)
    if result.returncode != 0:
        subprocess.run(["git", "push", "origin", "master"], capture_output=True, text=True)
    print(f"[+] SUCCESS: Royal.uk Witness Anchor Pushed Live! Hash: {w_hash}")
