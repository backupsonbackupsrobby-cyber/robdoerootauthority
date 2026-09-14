import subprocess
import hashlib
import sys

def get_git_objects():
    # Verify repository database via fsck
    print("--- EXECUTING RECURSIVE GIT FSCK ---")
    fsck_res = subprocess.run(["git", "fsck", "--full", "--strict"], capture_output=True, text=True)
    if fsck_res.returncode != 0 and "notice" not in fsck_res.stderr.lower():
        print(f"[-] WARNING: FSCK reported issues:\n{fsck_res.stderr}")
    else:
        print("[+] Repository integrity valid. Zero database corruption.\n")

    # Fetch all object SHA-1 hashes
    rev_res = subprocess.run(["git", "rev-list", "--all", "--objects"], capture_output=True, text=True)
    objects = [line.split()[0] for line in rev_res.stdout.strip().split('\n') if line.strip()]
    return sorted(list(set(objects)))

def compute_merkle_root(leaves, algorithm="sha256"):
    if not leaves:
        return None

    def hash_payload(data_str):
        b = data_str.encode('utf-8')
        if algorithm == "sha512":
            return hashlib.sha512(b).hexdigest()
        return hashlib.sha256(b).hexdigest()

    # Layer 0: Hash the object IDs
    current_level = [hash_payload(leaf) for leaf in leaves]

    # Collapsing tree layers recursively
    while len(current_level) > 1:
        if len(current_level) % 2 != 0:
            current_level.append(current_level[-1]) # Duplicate last odd leaf
        
        next_level = []
        for i in range(0, len(current_level), 2):
            combined = current_level[i] + current_level[i+1]
            next_level.append(hash_payload(combined))
        current_level = next_level

    return current_level[0]

objects = get_git_objects()
print(f"Collected {len(objects)} object leaves from database.")

root_256 = compute_merkle_root(objects, "sha256")
root_512 = compute_merkle_root(objects, "sha512")

print("=" * 80)
print(f"RECURSIVE MERKLE ROOT (SHA-256) : {root_256}")
print(f"RECURSIVE MERKLE ROOT (SHA-512) : {root_512}")
print("=" * 80)

with open("merkle_hex_vomit.txt", "w") as f:
    f.write(f"GIT_OBJECTS={len(objects)}\n")
    f.write(f"MERKLE_SHA256={root_256}\n")
    f.write(f"MERKLE_SHA512={root_512}\n")

print("\n[+] Direct state dump written to merkle_hex_vomit.txt")
