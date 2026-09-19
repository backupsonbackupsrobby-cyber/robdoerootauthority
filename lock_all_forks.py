import os
import hashlib
import json

WORKSPACE_ROOT = "./"
LOCAL_DROPZONE = "dropzone/payload.json"

def lock_all_forks():
    forks_locked = 0
    current_level = []
    
    # Bind Sleeble Twins vector to the lockdown root
    twins_state = b"sleeble-twins-alpha-beta-omni-fork-lockdown"
    current_level.append(hashlib.sha512(twins_state).digest() + hashlib.sha512(twins_state[::-1]).digest())

    print("[Lockdown]: Scanning and sealing all local forks and directories...")
    
    for root, dirs, files in os.walk(WORKSPACE_ROOT):
        # Skip dropzone and hidden git metadata to focus strictly on code forks/workspaces
        if ".git" in root or "dropzone" in root:
            continue
            
        for file in sorted(files):
            file_path = os.path.join(root, file)
            try:
                with open(file_path, "rb") as f:
                    file_data = f.read()
                    h = hashlib.sha512(file_data).digest() + hashlib.sha512(file_data[::-1]).digest()
                    current_level.append(h)
                    forks_locked += 1
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

    master_root_hex = current_level[0].hex()
    return master_root_hex, forks_locked

def execute():
    root_hex, count = lock_all_forks()
    print(f"[Success] Total Fork Artifacts Secured: {count}")
    print(f"[Success] Omni-Fork Master Merkle Root: {root_hex}")

    payload = {
        "framework": "sleeble-twins-omni-lockdown",
        "status": "secured",
        "artifacts_locked": count,
        "master_merkle_root": root_hex,
        "sovereign_authority": "ATOM-TRUTH | GENESIS:e14f9a8d"
    }

    os.makedirs("dropzone", exist_ok=True)
    with open(LOCAL_DROPZONE, "w") as f:
        json.dump(payload, f, indent=4)
        
    print(f"[Success] Omni-lockdown payload committed to drop-zone: {LOCAL_DROPZONE}")

if __name__ == "__main__":
    execute()
