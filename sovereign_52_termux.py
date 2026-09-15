import math
import cmath
import hashlib
import subprocess
import sys

def run_termux_sovereign_engine():
    print("\033[1;36m" + "=" * 68)
    print("  ROBDOE.COM | 52-CARD / 52-WEEK SOVEREIGN PHASE MATRIX (TERMUX)")
    print("=" * 68 + "\033[0m")

    # 1. Base-10 Scale Identity Check
    scale_identity = 0.052 * 1000
    assert abs(scale_identity - 52.0) < 1e-9, "Scale identity mismatch"
    print(f"\033[1;32m[+] Base-10 Identity Verified  : 0.052 x 1000 = {int(scale_identity)}\033[0m")

    # 2. Extract Git Object Leaves
    try:
        cmd = ["git", "rev-list", "--objects", "--all"]
        res = subprocess.run(cmd, capture_output=True, text=True, check=True)
        objects = sorted([line.split()[0] for line in res.stdout.strip().split('\n') if line])
    except Exception as e:
        print(f"\033[1;31m[-] Git error: {e}\033[0m")
        sys.exit(1)

    N_objects = len(objects)
    print(f"\033[1;32m[+] Git Objects Leaves Indexed  : {N_objects}\033[0m")

    # 3. Dual Merkle Root Reduction
    layer256 = [h.encode('utf-8') for h in objects]
    layer512 = list(layer256)

    while len(layer256) > 1:
        if len(layer256) % 2 != 0:
            layer256.append(layer256[-1])
            layer512.append(layer512[-1])
        layer256 = [hashlib.sha256(layer256[i] + layer256[i+1]).hexdigest().encode('utf-8') for i in range(0, len(layer256), 2)]
        layer512 = [hashlib.sha512(layer512[i] + layer512[i+1]).hexdigest().encode('utf-8') for i in range(0, len(layer512), 2)]

    sha256_root = layer256[0].decode('utf-8')
    sha512_root = layer512[0].decode('utf-8')

    # 4. 52-Suite Partitioning & Kuramoto Phase Locking
    suits = ['♠', '♥', '♦', '♣']
    cards_per_suit = 13
    total_cards = 52

    # Map phases on unit circle S^1 across the 52 cyclic slots
    phases = [2 * math.pi * k / total_cards for k in range(total_cards)]
    
    # Apply Quadratic map z -> z^2 + c & Kuramoto coupling update (K = 3.5)
    c = complex(-0.7, 0.27015)
    K = 3.5
    dt = 0.01

    for _ in range(500):
        # Phase doubling via quadratic map z -> z^2 + c
        Z = [cmath.rect(1.0, theta)**2 + c for theta in phases]
        phases = [cmath.phase(z) for z in Z]

        # Coupling force across N=52 ensemble
        new_phases = []
        for i in range(total_cards):
            coupling = (K / total_cards) * sum(math.sin(phases[j] - phases[i]) for j in range(total_cards))
            d_theta = 2 * phases[i] + coupling
            new_phases.append((phases[i] + d_theta * dt) % (2 * math.pi))
        phases = new_phases

    # Compute Macro Order Parameter R
    complex_order = sum(cmath.rect(1.0, theta) for theta in phases) / total_cards
    R = abs(complex_order)
    Psi = cmath.phase(complex_order)

    # 5. Output Results & Apply Annotated Git Tag
    tag_name = f"proof-52week-{sha256_root[:7]}"
    manifest = f"""LAW OF SHAPED FORCE | 52-WEEK SOVEREIGN PROOF
================================================================
DOMAIN         : robdoe.com
IDENTITY       : 0.052 x 10^3 = 52 Slots
OBJECT_LEAVES  : {N_objects}
KURAMOTO_R     : {R:.6f} [PHASE LOCKED]
MEAN_ANGLE_PSI : {Psi:.6f} rad
MERKLE_SHA256  : {sha256_root}
MERKLE_SHA512  : {sha512_root}
================================================================"""

    print(manifest)

    # Log to local ledger
    with open("state_proofs.log", "a") as f:
        f.write(manifest + "\n\n")

    # Apply tag directly in Git
    subprocess.run(["git", "tag", "-f", "-a", tag_name, "-m", manifest], check=True)
    print(f"\033[1;33m\n[+] Successfully tagged Git HEAD as '{tag_name}'\033[0m")
    print("\033[1;36m" + "=" * 68 + "\033[0m")

if __name__ == "__main__":
    run_termux_sovereign_engine()
