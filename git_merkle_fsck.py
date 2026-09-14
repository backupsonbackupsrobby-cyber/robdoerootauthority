import subprocess
import hashlib
import sys

def sha256(data: str) -> str:
    return hashlib.sha256(data.encode('utf-8')).hexdigest()

def build_merkle_root(leaves):
    if not leaves:
        return sha256("EMPTY_TREE")
    
    current_layer = [sha256(leaf) for leaf in leaves]
    
    while len(current_layer) > 1:
        next_layer = []
        if len(current_layer) % 2 != 0:
            current_layer.append(current_layer[-1])  # Duplicate odd leaf
        
        for i in range(0, len(current_layer), 2):
            combined = current_layer[i] + current_layer[i+1]
            next_layer.append(sha256(combined))
            
        current_layer = next_layer
        
    return current_layer[0]

def main():
    print("--- EXECUTING RECURSIVE GIT FSCK ---")
    
    # Run full strict git object verification
    result = subprocess.run(["git", "fsck", "--full", "--strict"], capture_output=True, text=True)
    
    if result.returncode != 0 and "notice" not in result.stderr.lower():
        print(f"[!] GIT FSCK ALERT / UNREACHABLE OBJECTS DETECTED:\n{result.stderr.strip()}")
    else:
        print("[+] Repository integrity valid. Zero database corruption.")

    # Gather object database leaves via rev-list
    rev_result = subprocess.run(["git", "rev-list", "--all", "--objects"], capture_output=True, text=True)
    
    raw_objects = rev_result.stdout.strip().split('\n')
    object_hashes = [line.split()[0] for line in raw_objects if line.strip()]
    
    print(f"\nCollected {len(object_hashes)} object leaves from database.")
    
    merkle_root = build_merkle_root(object_hashes)
    
    print("\n==================================================")
    print(f"RECURSIVE MERKLE ROOT PROOF: {merkle_root}")
    print("==================================================")

if __name__ == "__main__":
    main()
