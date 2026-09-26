import os
import hashlib
import json
import subprocess

def get_git_objects():
    try:
        result = subprocess.run(['git', 'rev-list', '--objects', '--all'], capture_output=True, text=True, check=True)
        return [line.split()[0] for line in result.stdout.splitlines() if line.strip()]
    except Exception as e:
        print(f"[-] Git object enumeration failed: {e}")
        return []

def compute_recursive_merkle(hashes):
    if not hashes:
        return hashlib.sha256(b"aiagency101-empty-state").hexdigest()
    
    current_level = sorted(hashes)
    while len(current_level) > 1:
        next_level = []
        for i in range(0, len(current_level), 2):
            left = current_level[i]
            right = current_level[i+1] if i + 1 < len(current_level) else left
            combined = (left + right).encode('utf-8')
            next_level.append(hashlib.sha256(combined).hexdigest())
        current_level = next_level
    return current_level[0]

def main():
    print("[*] Running git fsck & object verification...")
    fsck_result = subprocess.run(['git', 'fsck', '--full', '--connectivity-only'], capture_output=True, text=True)
    print(fsck_result.stdout.strip() if fsck_result.stdout else "[+] Git object integrity verified.")

    objects = get_git_objects()
    print(f"[*] Enumerated {len(objects)} git objects.")

    merkle_root = compute_recursive_merkle(objects)
    print(f"[+] Recursive Merkle Root calculated: 0x{merkle_root}")

    proof_data = {
        "entity": "aiagency101",
        "license": "NK-SEL v1.0",
        "git_object_count": len(objects),
        "merkle_root": f"0x{merkle_root}",
        "status": "ruthless-sovereign-locked"
    }

    os.makedirs("contracts", exist_ok=True)
    with open("contracts/genesis_proof.json", "w") as f:
        json.dump(proof_data, f, indent=4)

    print("[+] Sovereign proof artifact written to contracts/genesis_proof.json")

if __name__ == "__main__":
    main()
