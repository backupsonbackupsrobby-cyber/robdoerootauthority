#!/usr/bin/env python3
import os, sys, hashlib, subprocess

def hash_file(path):
    h = hashlib.sha512()
    try:
        with open(path, 'rb') as f:
            while chunk := f.read(1048576):
                h.update(chunk)
        return h.hexdigest()
    except Exception:
        return None

def main():
    target = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else ".")
    
    # OS-level fast file collection (ignoring heavy/hidden trees)
    cmd = [
        "find", target,
        "-type", "f",
        "-not", "-path", "*/.git/*",
        "-not", "-path", "*/spatial_stack_workspace/*",
        "-not", "-path", "*/__pycache__/*",
        "-not", "-path", "*/node_modules/*"
    ]
    
    res = subprocess.run(cmd, capture_output=True, text=True)
    files = sorted([f for f in res.stdout.split('\n') if f.strip()])
    
    if not files:
        print("ERROR: No files found to hash")
        return

    file_hashes = []
    for f in files:
        print(f"HASHING: {f}")
        h = hash_file(f)
        if h:
            file_hashes.append(h)

    # Binary Merkle Tree Reduction
    curr = file_hashes
    while len(curr) > 1:
        if len(curr) % 2 != 0:
            curr.append(curr[-1])
        curr = [hashlib.sha512((curr[i] + curr[i+1]).encode('utf-8')).hexdigest() for i in range(0, len(curr), 2)]

    root_hash = curr[0]
    tag_name = f"proof-{root_hash[:16]}"
    
    # Fast Git Tag
    subprocess.run(["git", "tag", "-f", "-a", tag_name, "-m", f"MERKLE_ROOT: {root_hash}"], cwd=target, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"\nSEALED:{tag_name}:{root_hash}")

if __name__ == "__main__":
    main()
