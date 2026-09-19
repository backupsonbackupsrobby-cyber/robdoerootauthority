import os
import hashlib
import json
import subprocess

LOCAL_DROPZONE = "dropzone/payload.json"

def check_git_status():
    print("[Audit]: Checking local Git repository and tracking lines...")
    try:
        result = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True, check=True)
        tracked = subprocess.run(["git", "ls-files"], capture_output=True, text=True, check=True)
        
        status_lines = result.stdout.strip().splitlines() if result.stdout.strip() else []
        tracked_files = tracked.stdout.strip().splitlines() if tracked.stdout.strip() else []
        
        print(f"[Audit]: Found {len(tracked_files)} tracked work files under Git authority.")
        return tracked_files
    except Exception as e:
        print(f"[Warning]: Git check failed or not a git repository: {e}")
        return []

def audit_and_hash_work():
    tracked_files = check_git_status()
    current_level = []
    
    # Sovereign permission anchor check
    sovereign_seal = b"ATOM-TRUTH-SOVEREIGN-WORK-AUTHORIZATION-CHECK"
    current_level.append(hashlib.sha512(sovereign_seal).digest() + hashlib.sha512(sovereign_seal[::-1]).digest())

    if tracked_files:
        for file_path in sorted(tracked_files):
            if os.path.exists(file_path):
                try:
                    with open(file_path, "rb") as f:
                        file_data = f.read()
                        h = hashlib.sha512(file_data).digest() + hashlib.sha512(file_data[::-1]).digest()
                        current_level.append(h)
                except Exception:
                    continue
    else:
        # Fallback to local directory walk if git check is empty
        for root, dirs, files in os.walk("./"):
            if ".git" in root or "dropzone" in root:
                continue
            for file in sorted(files):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "rb") as f:
                        file_data = f.read()
                        h = hashlib.sha512(file_data).digest() + hashlib.sha512(file_data[::-1]).digest()
                        current_level.append(h)
                except Exception:
                    continue

    while len(current_level) > 1:
        next_level = []
        for i in range(0, len(current_level), 2):
            left = current_level[i]
            right = current_level[i+1] if i + 1 < len(current_level) else left
            combined = hashlib.sha256(left + right).digest()
            next_level.append(combined)
        current_level = next_level

    audit_root = current_level[0].hex()
    print(f"[Success] Git-Bound Work Merkle Root: {audit_root}")

    payload = {
        "framework": "git-merkle-work-audit",
        "permission_status": "sovereign-local-exclusive",
        "master_merkle_root": audit_root,
        "sovereign_authority": "ATOM-TRUTH | GENESIS:e14f9a8d"
    }

    os.makedirs("dropzone", exist_ok=True)
    with open(LOCAL_DROPZONE, "w") as f:
        json.dump(payload, f, indent=4)
        
    print(f"[Success] Audit payload locked into drop-zone: {LOCAL_DROPZONE}")

if __name__ == "__main__":
    audit_and_hash_work()
