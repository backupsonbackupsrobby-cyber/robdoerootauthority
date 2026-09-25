import hashlib
import json
import subprocess
import os

def compute_root_hash():
    print("[*] Calculating cryptographic Merkle root hash across local artifacts...")
    files_to_hash = ["sovereign_miner.py", "xyo_proof.json"]
    file_hashes = {}

    for f in files_to_hash:
        if os.path.exists(f):
            with open(f, "rb") as file_obj:
                file_hashes[f] = hashlib.sha256(file_obj.read()).hexdigest()
        else:
            file_hashes[f] = "0" * 64

    combined_string = "".join([file_hashes[k] for k in sorted(file_hashes.keys())])
    root_hash = hashlib.sha256(combined_string.encode()).hexdigest()

    manifest = {
        "root_hash": root_hash,
        "components": file_hashes,
        "authority": "ATOM-TRUTH | RobDoe Pty Ltd"
    }

    with open("roothash_manifest.json", "w") as mf:
        json.dump(manifest, mf, indent=4)
        
    print(f"[+] Root Hash Hex Locked: {root_hash}")
    return root_hash

def one_shot_push(root_hash):
    print("[*] Executing atomic staging, commit, and one-shot push...")
    
    subprocess.run(["git", "add", "sovereign_miner.py", "xyo_proof.json", "roothash_manifest.json"], check=True)
    
    commit_msg = f"anchor(root): {root_hash} - ATOM-TRUTH sovereign synchronization"
    subprocess.run(["git", "commit", "-m", commit_msg], check=True)
    
    result = subprocess.run(["git", "push", "origin", "main"], capture_output=True, text=True)
    if result.returncode != 0:
        result = subprocess.run(["git", "push", "origin", "master"], capture_output=True, text=True)
        
    if result.returncode == 0:
        print("[+] SUCCESS: One-shot push executed and synchronized on-chain!")
    else:
        print("[-] Push encountered an upstream conflict or branch mismatch. Check remote status.")

if __name__ == "__main__":
    r_hash = compute_root_hash()
    one_shot_push(r_hash)
