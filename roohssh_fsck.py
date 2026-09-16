
import hashlib
import os

def sha512_iterative(data: bytes, iterations: int = 72) -> bytes:
    current = data
    for _ in range(iterations):
        current = hashlib.sha512(current).digest()
    return current

def compute_recursive_fsck_root(base_dir: str = ".") -> str:
    leaves = []
    for root, dirs, files in os.walk(base_dir):
        # Exclude git metadata and heavy externals
        if ".git" in root or "_external_dump" in root:
            continue
        for file in sorted(files):
            file_path = os.path.join(root, file)
            try:
                with open(file_path, "rb") as f:
                    content = f.read()
                # Apply sha512x72 to every file leaf
                sealed_leaf = sha512_iterative(content, 72)
                leaves.append(sealed_leaf)
            except Exception:
                continue

    if not leaves:
        return hashlib.sha512(b"EMPTY").digest().hex()

    current_level = leaves
    while len(current_level) > 1:
        next_level = []
        for i in range(0, len(current_level), 2):
            left = current_level[i]
            right = current_level[i + 1] if i + 1 < len(current_level) else left
            parent = hashlib.sha512(left + right).digest()
            next_level.append(parent)
        current_level = next_level

    return current_level[0].hex()

if __name__ == "__main__":
    print("[ROOHSSH-FS] Initializing recursive workspace fsck merkle seal...")
    root_hash = compute_recursive_fsck_root(".")
    print(f"[RECURSIVE MERKLE ROOT hex sha512x72]: {root_hash}")
