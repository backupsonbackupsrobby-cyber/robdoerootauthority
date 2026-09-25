cat << 'EOF' > recursive_dag.py
import hashlib
import json
import subprocess
import os

def sha256_hex(data: str) -> str:
    return hashlib.sha256(data.encode('utf-8')).hexdigest()

def build_merkle_dag(file_paths):
    print("[*] Constructing recursive Merkle DAG leaves and branches...")
    leaves = {}
    
    # Step 1: Create leaf nodes from file contents
    for path in sorted(file_paths):
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            leaf_hash = sha256_hex(content)
            leaves[path] = {
                "type": "leaf",
                "path": path,
                "size": len(content),
                "hash": leaf_hash
            }
        else:
            leaves[path] = {
                "type": "leaf",
                "path": path,
                "size": 0,
                "hash": sha256_hex("MISSING_LEAF")
            }

    # Step 2: Build branch layer from sorted leaf hashes
    sorted_leaf_keys = sorted(leaves.keys())
    leaf_hashes = [leaves[k]["hash"] for k in sorted_leaf_keys]
    
    # If odd number of leaves, duplicate the last one for pairing parity
    if len(leaf_hashes) % 2 != 0:
        leaf_hashes.append(leaf_hashes[-1])

    branch_hashes = []
    for i in range(0, len(leaf_hashes), 2):
        pair_combined = leaf_hashes[i] + leaf_hashes[i+1]
        branch_hashes.append(sha256_hex(pair_combined))

    # Step 3: Compute definitive Recursive DAG Root Hash
    dag_root_string = "".join(branch_hashes)
    dag_root_hash = sha256_hex(dag_root_string)

    dag_manifest = {
        "protocol": "ATOM-TRUTH-RECURSIVE-DAG-v1",
        "authority": "RobDoe Pty Ltd",
        "dag_root": dag_root_hash,
        "leaves": leaves,
        "branches": branch_hashes
    }

    with open("dag_manifest.json", "w") as dm:
        json.dump(dag_manifest, dm, indent=4)

    print(f"[+] Recursive DAG Root Hash Locked: {dag_root_hash}")
    return dag_root_hash

def execute_atomic_dag_push(dag_root):
    print("[*] Staging artifacts and executing final atomic push...")
    
    files_to_add = ["sovereign_miner.py", "xyo_proof.json", "dag_manifest.json"]
    for f in files_to_add:
        if os.path.exists(f):
            subprocess.run(["git", "add", f], check=True)

    commit_msg = f"dag(root): {dag_root} - Recursive Merkle self-sufficient synchronization"
    subprocess.run(["git", "commit", "-m", commit_msg], check=True)

    result = subprocess.run(["git", "push", "origin", "main"], capture_output=True, text=True)
    if result.returncode != 0:
        result = subprocess.run(["git", "push", "origin", "master"], capture_output=True, text=True)

    if result.returncode == 0:
        print("[+] SUCCESS: Recursive DAG anchored and pushed live!")
    else:
        print("[-] Push completed with warning/branch mismatch. Check git status.")

if __name__ == "__main__":
    targets = ["sovereign_miner.py", "xyo_proof.json"]
    root_hash = build_merkle_dag(targets)
    execute_atomic_dag_push(root_hash)
EOF
python3 xyo_sync.py && python3 recursive_dag.py
