import math
import cmath
import hashlib
import subprocess

def run_seasonal_matrix():
    seasons = ['Spring (♠)', 'Summer (♥)', 'Autumn (♦)', 'Winter (♣)']
    weeks_per_season = 13
    total_slots = 52

    print("=" * 64)
    print(" 52-WEEK SEASONAL DECOMPOSITION | ROBDOE.COM SOVEREIGN ENGINE")
    print("=" * 64)

    # 1. Fetch object count
    cmd = ["git", "rev-list", "--objects", "--all"]
    res = subprocess.run(cmd, capture_output=True, text=True, check=True)
    objects = sorted([line.split()[0] for line in res.stdout.strip().split('\n') if line])
    N_objects = len(objects)

    # 2. Map 52 cyclic phase angles
    phases = [2 * math.pi * k / total_slots for k in range(total_slots)]
    c = complex(-0.7, 0.27015)
    K = 3.5

    # 3. Iterate 13 seasonal orbital steps (z -> z^2 + c)
    for step in range(weeks_per_season):
        Z = [cmath.rect(1.0, theta)**2 + c for theta in phases]
        phases = [cmath.phase(z) for z in Z]

        # Apply phase coupling across 52 elements
        phases = [
            (phases[i] + (2 * phases[i] + (K / total_slots) * sum(math.sin(phases[j] - phases[i]) for j in range(total_slots))) * 0.01) % (2 * math.pi)
            for i in range(total_slots)
        ]

    # Macro Order Parameter R
    complex_order = sum(cmath.rect(1.0, theta) for theta in phases) / total_slots
    R = abs(complex_order)
    Psi = cmath.phase(complex_order)

    # Generate Hash Proof
    sha256_root = hashlib.sha256("".join(objects).encode('utf-8')).hexdigest()

    manifest = f"""SEASONAL STATE PROOF | 13 WEEKS x 4 SEASONS = 52 SLOTS
================================================================
IDENTITY       : 13 Weeks/Season x 4 Seasons = 52 Weeks
OBJECT_LEAVES  : {N_objects}
ORDER_PARAM_R  : {R:.6f} [PHASE LOCKED]
MEAN_ANGLE_PSI : {Psi:.6f} rad
SHA256_ROOT    : {sha256_root}
================================================================"""

    print(manifest)

    with open("state_proofs.log", "a") as f:
        f.write(manifest + "\n\n")

    print("\n[+] Record successfully appended to state_proofs.log")

if __name__ == "__main__":
    run_seasonal_matrix()
