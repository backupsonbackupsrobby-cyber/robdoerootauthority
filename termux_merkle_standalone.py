#!/usr/bin/env python3
import os, sys, hashlib, json
from pathlib import Path

def calculate_file_hash(filepath):
    """Generates SHA-512 leaf hash using streaming chunks."""
    hasher = hashlib.sha512()
    try:
        with open(filepath, 'rb') as f:
            while chunk := f.read(1048576):
                hasher.update(chunk)
        return hasher.hexdigest()
    except Exception:
        return None

def build_merkle_root(leaf_hashes):
    """Recursively computes binary SHA-512 Merkle root."""
    if not leaf_hashes:
        return hashlib.sha512(b"EMPTY_TREE").hexdigest()
    
    current_level = sorted(leaf_hashes)
    while len(current_level) > 1:
        if len(current_level) % 2 != 0:
            current_level.append(current_level[-1])
            
        next_level = []
        for i in range(0, len(current_level), 2):
            combined = (current_level[i] + current_level[i+1]).encode('utf-8')
            parent_hash = hashlib.sha512(combined).hexdigest()
            next_level.append(parent_hash)
        current_level = next_level
        
    return current_level[0]

def audit_directory(target_dir):
    ignore_dirs = {'.git', '__pycache__', 'node_modules', '.venv', 'spatial_stack_workspace'}
    target = Path(target_dir).resolve()
    leaf_map = {}
    
    for root, dirs, files in os.walk(target):
        dirs[:] = [d for d in dirs if d not in ignore_dirs]
        for file in files:
            full_path = Path(root) / file
            rel_path = str(full_path.relative_to(target))
            file_hash = calculate_file_hash(full_path)
            if file_hash:
                leaf_map[rel_path] = file_hash

    hashes = list(leaf_map.values())
    merkle_root = build_merkle_root(hashes)
    
    return {
        "status": "SEALED",
        "target_directory": str(target),
        "total_files": len(leaf_map),
        "merkle_root": merkle_root
    }

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "."
    res = audit_directory(target)
    print(json.dumps(res, indent=2))
