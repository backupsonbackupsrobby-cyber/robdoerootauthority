import os
import hashlib
import json
import time

def hash_file(filepath):
    hasher = hashlib.sha512()
    try:
        with open(filepath, "rb") as f:
            while chunk := f.read(8192):
                hasher.update(chunk)
        return hasher.hexdigest()
    except Exception:
        return None

def build_master_merkle_tree():
    root_dir = "."
    file_hashes = {}
    
    for root, dirs, files in os.walk(root_dir):
        # Skip git internals
        if ".git" in root:
            continue
        for file in files:
            filepath = os.path.join(root, file)
            rel_path = os.path.relpath(filepath, root_dir)
            file_hash = hash_file(filepath)
            if file_hash:
                file_hashes[rel_path] = file_hash

    # Sort and compute master SHA-512 root
    sorted_manifest = sorted(file_hashes.items())
    master_hasher = hashlib.sha512()
    for path, fhash in sorted_manifest:
        master_hasher.update(f"{path}:{fhash}".encode("utf-8"))
    
    master_root = master_hasher.hexdigest()
    
    manifest_data = {
        "timestamp": int(time.time()),
        "total_files": len(file_hashes),
        "master_sha512_merkle_root": master_root,
        "files": file_hashes
    }
    
    with open("master_grid_root.json", "w") as f:
        json.dump(manifest_data, f, indent=2)
        
    print("===================================================")
    print("  [MASTER MERKLE] : ALL NODES & SUBS LOCKED")
    print("===================================================")
    print(f"Master Root Hash : {master_root}")
    print(f"Total Tracked    : {len(file_hashes)} files/modules")
    print("===================================================")

if __name__ == "__main__":
    build_master_merkle_tree()
