#!/usr/bin/env python3
import os, sys, hashlib, math, subprocess

def collatz_orbit_energy(n):
    """Calculates non-linear kinetic energy from the 3n+1 trajectory length & peak."""
    steps = 0
    peak = n
    curr = n
    while curr > 1 and steps < 1000:
        if curr % 2 == 0:
            curr = curr // 2
        else:
            curr = 3 * curr + 1
        if curr > peak:
            peak = curr
        steps += 1
    # Normalized Kinetic Energy Output: (orbit_length * log(peak))
    return float(steps) * math.log(max(peak, 2))

def main():
    target = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else ".")
    
    # 1. Fast Directory Collect
    cmd = ["find", target, "-type", "f", "-not", "-path", "*/.git/*", "-not", "-path", "*/spatial_stack_workspace/*"]
    res = subprocess.run(cmd, capture_output=True, text=True)
    files = sorted([f for f in res.stdout.split('\n') if f.strip()])

    if not files:
        print("ERROR: Empty target.")
        return

    # 2. Merkle Root Generation
    hashes = []
    for f in files:
        h = hashlib.sha512()
        try:
            with open(f, 'rb') as fp:
                while chunk := fp.read(1048576):
                    h.update(chunk)
            hashes.append(h.hexdigest())
        except Exception:
            pass

    curr = hashes if hashes else [hashlib.sha512(b"EMPTY").hexdigest()]
    while len(curr) > 1:
        if len(curr) % 2 != 0:
            curr.append(curr[-1])
        curr = [hashlib.sha512((curr[i] + curr[i+1]).encode()).hexdigest() for i in range(0, len(curr), 2)]
    
    merkle_root = curr[0]
    raw_bytes = bytes.fromhex(merkle_root)
    N = len(raw_bytes) # 64 nodes

    # 3. 3n+1 Kinetic Energy Modulation of Frequencies (omega_i)
    theta = [(b / 255.0) * 2.0 * math.pi for b in raw_bytes]
    # Seed 3n+1 trajectory with byte values (ensuring non-zero start n = b + 1)
    collatz_energies = [collatz_orbit_energy(b + 1) for b in raw_bytes]
    max_energy = max(collatz_energies) if max(collatz_energies) > 0 else 1.0
    
    # Kinetic frequencies driven by 3n+1 orbits
    omega = [(e / max_energy) * 10.0 for e in collatz_energies]

    # 4. Phase Coupling Integration (Kuramoto Lock)
    K = 1.5 # Higher coupling constant to absorb Collatz kinetic energy
    dt = 0.01
    for _ in range(500):
        dtheta = [omega[i] + (K / N) * sum(math.sin(theta[j] - theta[i]) for j in range(N)) for i in range(N)]
        theta = [(theta[i] + dtheta[i] * dt) % (2.0 * math.pi) for i in range(N)]

    # 5. Calculate Order Parameter R
    real_part = sum(math.cos(th) for th in theta) / N
    imag_part = sum(math.sin(th) for th in theta) / N
    R = math.hypot(real_part, imag_part)

    proof_hash = hashlib.sha512(f"3N1_PROOF|{merkle_root}|R:{R:.10f}".encode()).hexdigest()
    tag_name = f"proof-3n1-{proof_hash[:12]}"
    
    # Direct safe tag seal
    subprocess.run(["git", "tag", "-f", "-a", tag_name, "-m", f"MERKLE_ROOT: {merkle_root}\nKURAMOTO_R: {R:.10f}\nCOLLATZ_KINETIC: ACTIVE"], cwd=target, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    print(f"COLLATZ_3N1_KINETIC_ENGAGED")
    print(f"MERKLE_ROOT:{merkle_root[:16]}...")
    print(f"PHASE_COHERENCE_R:{R:.10f}")
    print(f"TAG_SEALED:{tag_name}")

if __name__ == "__main__":
    main()
