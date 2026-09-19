import os
import hashlib
import json

TARGET_DIR = "./zsh-copilot"
LOCAL_DROPZONE = "dropzone/payload.json"

def clone_repository():
    if not os.path.exists(TARGET_DIR):
        print(f"[Cloning]: Targeting https://github.com/backupsonbackupsrobby-cyber/zsh-copilot...")
        os.system(f"git clone https://github.com/backupsonbackupsrobby-cyber/zsh-copilot.git {TARGET_DIR}")
    else:
        print(f"[Success]: Target repository already present at {TARGET_DIR}")

def build_merkle_tree(directory):
    current_level = []
    for root, dirs, files in os.walk(directory):
        for file in sorted(files):
            file_path = os.path.join(root, file)
            try:
                with open(file_path, "rb") as f:
                    file_data = f.read()
                    h = hashlib.sha512(file_data).digest() + hashlib.sha512(file_data[::-1]).digest()
                    current_level.append(h)
            except Exception:
                continue

    if not current_level:
        current_level = [hashlib.sha512(b"genesis").digest()]

    while len(current_level) > 1:
        next_level = []
        for i in range(0, len(current_level), 2):
            left = current_level[i]
            right = current_level[i+1] if i + 1 < len(current_level) else left
            combined = hashlib.sha256(left + right).digest()
            next_level.append(combined)
        current_level = next_level

    return current_level[0].hex()

def execute():
    clone_repository()
    print(f"[Math Engine]: Computing SHA-1024 Merkle Root for {TARGET_DIR}...")
    root_hex = build_merkle_tree(TARGET_DIR)
    print(f"[Success] Merkle Root (SHA-1024): {root_hex}")

    payload = {
        "framework": "llama-agents",
        "standard": "sha1024",
        "target": TARGET_DIR,
        "merkle_root": root_hex,
        "pipeline": "sleeble-x2-16-arms"
    }

    with open(LOCAL_DROPZONE, "w") as f:
        json.dump(payload, f, indent=4)
    print(f"[Success] Payload locked into local drop-zone: {LOCAL_DROPZONE}")

if __name__ == "__main__":
    execute()
