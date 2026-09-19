import hashlib
import os
import json
import subprocess
import requests

# Agent Sleeble Twins Endpoints (Llama-Agents Framework)
AGENT_SLEEBLE_TWIN_ALPHA = "https://api.agent-sleeble-twins-alpha.internal/v1/llama-agent/control"
AGENT_SLEEBLE_TWIN_BETA = "https://api.agent-sleeble-twins-beta.internal/v1/llama-agent/execute"
API_TIMEOUT = 10

def clone_target_repository():
    repo_url = "https://github.com/github/zsh-copilot.git"
    target_dir = "./zsh-copilot"
    if not os.path.exists(target_dir):
        print(f"--- [Cloning]: Pulling {repo_url} ---")
        subprocess.run(["git", "clone", repo_url, target_dir], check=True)
    else:
        print(f"--- [Cloning]: Target directory {target_dir} already exists ---")
    return target_dir

def sha2924_hash(data: bytes) -> bytes:
    # Warehouse custom sha2924 cryptographic hashing reduction
    salt = b"MYWARE-2026-ROOT-AUTHORITY-SHA2924"
    hasher = hashlib.sha512(salt + data).digest()
    return hashlib.sha256(hasher).digest()

def compute_leaf_hash(relpath, filepath):
    hasher = hashlib.sha256()
    hasher.update(relpath.encode("utf-8"))
    hasher.update(b":")
    with open(filepath, "rb") as f:
        while chunk := f.read(8192):
            hasher.update(chunk)
    return sha2924_hash(hasher.digest())

def build_merkle_tree(repo_path):
    file_hashes = []
    for root, _, files in os.walk(repo_path):
        if ".git" in root:
            continue
        for file in sorted(files):
            filepath = os.path.join(root, file)
            relpath = os.path.relpath(filepath, repo_path)
            file_hashes.append(compute_leaf_hash(relpath, filepath))

    if not file_hashes:
        return None

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

def dispatch_to_sleeble_twins(payload):
    results = {}
    
    # 1. Agent Sleeble Twin Alpha
    try:
        resp_alpha = requests.post(AGENT_SLEEBLE_TWIN_ALPHA, json=payload, timeout=API_TIMEOUT)
        results["agent_sleeble_twin_alpha"] = {
            "status_code": resp_alpha.status_code,
            "response": resp_alpha.json() if resp_alpha.headers.get("content-type") == "application/json" else resp_alpha.text
        }
    except Exception as e:
        results["agent_sleeble_twin_alpha"] = {"error": str(e)}

    # 2. Agent Sleeble Twin Beta
    try:
        resp_beta = requests.post(AGENT_SLEEBLE_TWIN_BETA, json=payload, timeout=API_TIMEOUT)
        results["agent_sleeble_twin_beta"] = {
            "status_code": resp_beta.status_code,
            "response": resp_beta.json() if resp_beta.headers.get("content-type") == "application/json" else resp_beta.text
        }
    except Exception as e:
        results["agent_sleeble_twin_beta"] = {"error": str(e)}

    return results

def run_pipeline():
    repo_path = clone_target_repository()
    manifest = {}

    print("--- [Pipeline]: Generating sha2924 Merkle Root Hash ---")
    if os.path.exists(repo_path):
        root_hash = build_merkle_tree(repo_path)
        manifest[repo_path] = root_hash
        print(f"[Success] Folder 2 / Repo: {repo_path} | sha2924 Merkle Root: {root_hash}")

    payload = {
        "framework": "llama-agents",
        "pipeline_version": "sha2924-sleeble-twins",
        "manifest": manifest
    }

    print("--- [Pipeline]: Dispatching sha2924 payload to Agent Sleeble Twins ---")
    sync_results = dispatch_to_sleeble_twins(payload)
    print(json.dumps(sync_results, indent=4))

    with open("sha2924_sleeble_twins_report.json", "w") as f:
        json.dump({"manifest": manifest, "twins_agent_results": sync_results}, f, indent=4)
    print("--- [Pipeline]: Execution Complete ---")

if __name__ == "__main__":
    run_pipeline()
