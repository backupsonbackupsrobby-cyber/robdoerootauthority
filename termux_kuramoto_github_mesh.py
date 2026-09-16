#!/usr/bin/env python3
import os, sys, hashlib, math, subprocess, json

def get_clean_file_list(target):
    cmd = [
        "find", target, "-type", "f",
        "-not", "-path", "*/.git/*",
        "-not", "-path", "*/spatial_stack_workspace/*",
        "-not", "-path", "*/__pycache__/*",
        "-not", "-path", "*/node_modules/*"
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    return sorted([f for f in res.stdout.split('\n') if f.strip()])

def stream_sha512(path):
    h = hashlib.sha512()
    try:
        with open(path, 'rb') as f:
            while chunk := f.read(1048576):
                h.update(chunk)
        return h.hexdigest()
    except Exception:
        return None

def compute_merkle_root(leaf_hashes):
    if not leaf_hashes:
        return hashlib.sha512(b"EMPTY_TREE").hexdigest()
    curr = leaf_hashes
    while len(curr) > 1:
        if len(curr) % 2 != 0:
            curr.append(curr[-1])
        curr = [hashlib.sha512((curr[i] + curr[i+1]).encode('utf-8')).hexdigest() for i in range(0, len(curr), 2)]
    return curr[0]

def solve_kuramoto_photon_lattice(merkle_root_hex):
    # 1. Map 64 byte nodes into phase angles theta in [0, 2pi]
    raw_bytes = bytes.fromhex(merkle_root_hex)
    N = len(raw_bytes) # 64 oscillators
    
    theta = [(b / 255.0) * 2.0 * math.pi for b in raw_bytes]
    
    # 2. Photon frequency mapping (Visible spectrum 400nm - 700nm -> energy omega = E/hbar)
    c = 3.0e8
    omega = [(2.0 * math.pi * c / ((400.0 + (b / 255.0) * 300.0) * 1.0e-9)) * 1.0e-15 for b in raw_bytes]

    # 3. Phase coupling integration loop
    K = 0.5
    dt = 0.01
    steps = 1000

    for _ in range(steps):
        dtheta = [0.0] * N
        for i in range(N):
            coupling = sum(math.sin(theta[j] - theta[i]) for j in range(N))
            dtheta[i] = omega[i] + (K / N) * coupling
        for i in range(N):
            theta[i] = (theta[i] + dtheta[i] * dt) % (2.0 * math.pi)

    # 4. Complex Order Parameter R (Phase Coherence Metric)
    real_part = sum(math.cos(th) for th in theta) / N
    imag_part = sum(math.sin(th) for th in theta) / N
    R = math.hypot(real_part, imag_part)
    psi = math.atan2(imag_part, real_part)
    
    return R, psi

def main():
    target = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else ".")
    print(f"[+] Processing Target: {target}")

    # Step A: Collect regular files & hash leaves
    files = get_clean_file_list(target)
    leaf_hashes = []
    for f in files:
        h = stream_sha512(f)
        if h:
            leaf_hashes.append(h)

    # Step B: Merkle Tree Hash Proof
    merkle_root = compute_merkle_root(leaf_hashes)

    # Step C: Kuramoto Photon Coherence Equation
    R, psi = solve_kuramoto_photon_lattice(merkle_root)

    # Step D: Cryptographic Seal
    proof_payload = f"TERMUX_FORM_PROOF|ROOT:{merkle_root}|R:{R:.12f}|PSI:{psi:.12f}".encode('utf-8')
    proof_sha512 = hashlib.sha512(proof_payload).hexdigest()
    
    tag_name = f"proof-kuramoto-{proof_sha512[:12]}"
    tag_msg = (
        f"MERKLE_ROOT: {merkle_root}\n"
        f"KURAMOTO_R: {R:.12f}\n"
        f"PHOTON_PSI: {psi:.12f}\n"
        f"PROOF_SHA512: {proof_sha512}"
    )

    # Step E: Bound to Git Tag via Safe Parameter Arrays
    try:
        subprocess.run(["git", "tag", "-f", "-a", tag_name, "-m", tag_msg], cwd=target, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"SEALED:{tag_name}")
        print(f"MERKLE_ROOT:{merkle_root}")
        print(f"KURAMOTO_COHERENCE_R:{R:.12f}")
    except Exception as e:
        print(f"ERROR:{e}")

if __name__ == "__main__":
    main()
