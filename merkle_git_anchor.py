import os
import hashlib
import subprocess
from pathlib import Path

ROOT_DIR = Path.cwd()
IDENTITY_ANCHOR = "ko_te_mana_o_te_tangata"
EXCLUDE_DIRS = {".git", "node_modules", "vendor", ".venv", "dist", "build"}

def compute_file_hash(filepath):
    sha256 = hashlib.sha256()
    try:
        with open(filepath, "rb") as f:
            while chunk := f.read(8192):
                sha256.update(chunk)
        return sha256.hexdigest()
    except Exception:
        return None

def build_merkle_root():
    file_hashes = []
    for path in sorted(ROOT_DIR.rglob("*")):
        if any(exc in path.parts for exc in EXCLUDE_DIRS):
            continue
        if path.is_file() and not any(part.startswith('.') for part in path.parts):
            if path.name == "merkle_git_anchor.py":
                continue
            f_hash = compute_file_hash(path)
            if f_hash:
                file_hashes.append(f_hash.encode('utf-8'))
                
    if not file_hashes:
        return hashlib.sha256(b"EMPTY_LATTICE").hexdigest()

    # Simple binary Merkle reduction tree
    current_level = file_hashes
    while len(current_level) > 1:
        next_level = []
        for i in range(0, len(current_level), 2):
            left = current_level[i]
            right = current_level[i+1] if i + 1 < len(current_level) else left
            combined = hashlib.sha256(left + right).digest()
            next_level.append(combined)
        current_level = next_level
        
    return current_level[0].hex()

if __name__ == "__main__":
    print("--- COMPUTING LOCAL MERKLE ROOT ---")
    merkle_root = build_merkle_root()
    print(f"Merkle Root Hash: {merkle_root}")
    
    # Anchor into Git Ledger
    manifest_path = ROOT_DIR / "MERKLE_ROOT.lock"
    manifest_path.write_text(f"ANCHOR: {IDENTITY_ANCHOR}\nMERKLE_ROOT: {merkle_root}\n")
    
    subprocess.run(["git", "add", "MERKLE_ROOT.lock"], stdout=subprocess.DEVNULL)
    subprocess.run(["git", "commit", "-m", f"SOVEREIGN_ANCHOR: {merkle_root}"], stdout=subprocess.DEVNULL)
    
    git_tree = subprocess.run(["git", "write-tree"], stdout=subprocess.PIPE, text=True).stdout.strip()
    print(f"Git Ledger Tree Anchored: {git_tree}")
    print(f"Status: Self-sufficient and locked under {IDENTITY_ANCHOR}.")
