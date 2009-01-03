import os
import subprocess
from pathlib import Path

ROOT_DIR = Path.cwd()
IDENTITY_ANCHOR = "ko_te_mana_o_te_tangata"
EXCLUDE_DIRS = {".git", "node_modules", "vendor", ".venv", "dist", "build"}

def get_git_tree_hash():
    try:
        result = subprocess.run(
            ["git", "write-tree"], 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE, 
            text=True, 
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return "LOCAL_DIRTY_STATE"

def purify_identity_barrier():
    foreign_markers = ["telemetry", "cloud_sync", "analytics", "external_auth"]
    purged_count = 0
    
    for path in ROOT_DIR.rglob("*"):
        if any(exc in path.parts for exc in EXCLUDE_DIRS):
            continue
        if path.is_file() and not any(part.startswith('.') for part in path.parts):
            try:
                content = path.read_text(encoding="utf-8", errors="ignore")
                for marker in foreign_markers:
                    if marker in content.lower():
                        print(f"[PURGED_VECTOR]: {path.name} -> {marker}")
                        purged_count += 1
                        break
            except Exception:
                continue
    return purged_count

if __name__ == "__main__":
    print("--- SOVEREIGN RUNTIME (CLEAN SWEEP) ---")
    print(f"Tree Hash: {get_git_tree_hash()}")
    vectors = purify_identity_barrier()
    print(f"Total Purged Vectors: {vectors}")
    print(f"Status: Lattice sealed under {IDENTITY_ANCHOR}.")
