#!/usr/bin/env python3
import os, sys, hashlib, math, json, subprocess

def collect_pure_leaves(target):
    cmd = [
        "find", target, "-type", "f",
        "-not", "-path", "*/.git/*",
        "-not", "-path", "*/spatial_stack_workspace/*",
        "-not", "-path", "*/__pycache__/*",
        "-not", "-path", "*/node_modules/*"
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    return sorted([f for f in res.stdout.split('\n') if f.strip()])

def stream_sha512(filepath):
    h = hashlib.sha512()
    try:
        with open(filepath, 'rb') as fp:
            while chunk := fp.read(1048576):
                h.update(chunk)
        return h.hexdigest()
    except Exception:
        return None

def execute_720_pass_cascade(base_root_hex):
    """
    Executes a 720-pass recursive SHA-512 state cascade.
    Simulates high-density rotational hashing across a 720-degree phase field.
    """
    state = bytes.fromhex(base_root_hex)
    history_chain = [base_root_hex]
    
    for iteration in range(1, 721):
        hasher = hashlib.sha512()
        # Mix iteration step integer into binary state vector
        hasher.update(state)
        hasher.update(iteration.to_bytes(4, byteorder='big'))
        state = hasher.digest()
        if iteration % 120 == 0 or iteration == 720:
            history_chain.append(state.hex())
            
    return state.hex(), history_chain

def build_merkle_root(leaf_hashes):
    if not leaf_hashes:
        return hashlib.sha512(b"EMPTY_CANON").hexdigest()
    curr = sorted(leaf_hashes)
    while len(curr) > 1:
        if len(curr) % 2 != 0:
            curr.append(curr[-1])
        curr = [hashlib.sha512((curr[i] + curr[i+1]).encode('utf-8')).hexdigest() for i in range(0, len(curr), 2)]
    return curr[0]

def main():
    target = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else ".")
    print(f"[+] Initializing SHA-512x720 Rotational Root Authority: {target}")

    files = collect_pure_leaves(target)
    leaf_hashes = []
    for f in files:
        h = stream_sha512(f)
        if h:
            leaf_hashes.append(h)

    # 1. Base Binary Merkle Root
    base_merkle = build_merkle_root(leaf_hashes)
    
    # 2. 720-Pass Cryptographic Cascade
    final_x720_root, checkpoints = execute_720_pass_cascade(base_merkle)
    
    # 3. Form Tag Payload
    proof_payload = {
        "status": "SEALED_720_PASS",
        "total_leaves": len(leaf_hashes),
        "base_merkle_root": base_merkle,
        "sha512_x720_root": final_x720_root,
        "checkpoints_count": len(checkpoints)
    }

    tag_name = f"proof-x720-{final_x720_root[:12]}"
    tag_msg = (
        f"BASE_MERKLE_ROOT: {base_merkle}\n"
        f"SHA512_X720_ROOT: {final_x720_root}\n"
        f"TOTAL_LEAVES: {len(leaf_hashes)}\n"
        f"CASCADE_PASSES: 720"
    )

    # 4. Bind to Git Tag using Parameterized Subprocess
    try:
        subprocess.run(["git", "tag", "-f", "-a", tag_name, "-m", tag_msg], cwd=target, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(json.dumps(proof_payload, indent=2))
        print(f"\n[+] SEALED_TAG: {tag_name}")
    except Exception as e:
        print(f"[!] Error sealing tag: {e}")

if __name__ == "__main__":
    main()
