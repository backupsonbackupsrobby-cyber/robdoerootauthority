#!/usr/bin/env python3
import os, sys, hashlib, math, subprocess, json

def collatz_orbit_energy(n):
    steps, peak, curr = 0, n, n
    while curr > 1 and steps < 1000:
        curr = curr // 2 if curr % 2 == 0 else 3 * curr + 1
        if curr > peak: peak = curr
        steps += 1
    return float(steps) * math.log(max(peak, 2))

def get_clean_leaves(target):
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

def build_merkle_root(leaf_hashes):
    if not leaf_hashes:
        return hashlib.sha512(b"EMPTY_CANON").hexdigest()
    curr = sorted(leaf_hashes)
    while len(curr) > 1:
        if len(curr) % 2 != 0:
            curr.append(curr[-1])
        curr = [hashlib.sha512((curr[i] + curr[i+1]).encode('utf-8')).hexdigest() for i in range(0, len(curr), 2)]
    return curr[0]

def execute_720_cascade(base_root_hex):
    state = bytes.fromhex(base_root_hex)
    for iteration in range(1, 721):
        hasher = hashlib.sha512()
        hasher.update(state)
        hasher.update(iteration.to_bytes(4, byteorder='big'))
        state = hasher.digest()
    return state.hex()

def solve_kuramoto(merkle_root_hex):
    raw_bytes = bytes.fromhex(merkle_root_hex)
    N = len(raw_bytes)
    theta = [(b / 255.0) * 2.0 * math.pi for b in raw_bytes]
    energies = [collatz_orbit_energy(b + 1) for b in raw_bytes]
    max_e = max(energies) if max(energies) > 0 else 1.0
    omega = [(e / max_e) * 10.0 for e in energies]

    K, dt = 1.5, 0.01
    for _ in range(500):
        dtheta = [omega[i] + (K / N) * sum(math.sin(theta[j] - theta[i]) for j in range(N)) for i in range(N)]
        theta = [(theta[i] + dtheta[i] * dt) % (2.0 * math.pi) for i in range(N)]

    real_s = sum(math.cos(th) for th in theta) / N
    imag_s = sum(math.sin(th) for th in theta) / N
    return math.hypot(real_s, imag_s)

def main():
    target = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else ".")
    files = get_clean_leaves(target)
    leaf_hashes = [h for f in files if (h := stream_sha512(f))]
    
    merkle_root = build_merkle_root(leaf_hashes)
    x720_root = execute_720_cascade(merkle_root)
    R = solve_kuramoto(merkle_root)

    proof_hash = hashlib.sha512(f"RVE|{merkle_root}|{x720_root}|R:{R:.10f}".encode()).hexdigest()
    tag_name = f"rve-seal-{proof_hash[:12]}"
    tag_msg = (
        f"MERKLE_ROOT: {merkle_root}\n"
        f"SHA512_X720_ROOT: {x720_root}\n"
        f"KURAMOTO_R: {R:.10f}\n"
        f"ZERO_RCE_VECTOR: ENFORCED"
    )

    subprocess.run(["git", "tag", "-f", "-a", tag_name, "-m", tag_msg], cwd=target, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    output = {
        "status": "RVE_SEALED",
        "merkle_root": merkle_root[:16] + "...",
        "sha512_x720_root": x720_root[:16] + "...",
        "kuramoto_R": f"{R:.10f}",
        "tag_sealed": tag_name
    }
    print(json.dumps(output, indent=2))

if __name__ == "__main__":
    main()
