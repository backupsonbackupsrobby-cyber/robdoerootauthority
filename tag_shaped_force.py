import cmath
import math
import hashlib
import subprocess

def apply_law_of_shaped_force():
    # 1. Fetch all raw Git object leaves
    cmd = ["git", "rev-list", "--objects", "--all"]
    res = subprocess.run(cmd, capture_output=True, text=True, check=True)
    objects = sorted([line.split()[0] for line in res.stdout.strip().split('\n') if line])
    N = len(objects)

    # 2. Compute Dual-Hash Merkle Roots (Sha256 / Sha512)
    layer256 = [h.encode() for h in objects]
    layer512 = list(layer256)

    while len(layer256) > 1:
        if len(layer256) % 2 != 0:
            layer256.append(layer256[-1])
            layer512.append(layer512[-1])
        layer256 = [hashlib.sha256(layer256[i] + layer256[i+1]).hexdigest().encode() for i in range(0, len(layer256), 2)]
        layer512 = [hashlib.sha512(layer512[i] + layer512[i+1]).hexdigest().encode() for i in range(0, len(layer512), 2)]

    sha256_root = layer256[0].decode()
    sha512_root = layer512[0].decode()

    # 3. Shape Force: Complex Phase Vector Reduction
    phases = [(int(h[:8], 16) / 0xFFFFFFFF) * 2 * math.pi for h in objects]
    complex_order = sum(cmath.rect(1.0, theta) for theta in phases) / N
    R = abs(complex_order)
    Psi = cmath.phase(complex_order)

    # 4. Construct Manifest Payload
    tag_name = f"proof-shaped-{sha256_root[:7]}"
    manifest = f"""LAW OF SHAPED FORCE | SOVEREIGN MERKLE PROOF
================================================================
DOMAIN         : robdoe.com
OBJECT_LEAVES  : {N}
ORDER_PARAM_R  : {R:.6f}
MEAN_ANGLE_PSI : {Psi:.6f} rad
MERKLE_SHA256  : {sha256_root}
MERKLE_SHA512  : {sha512_root}
================================================================"""

    print(manifest)

    # Write to local proof artifact
    with open("shaped_force_proof.txt", "w") as f:
        f.write(manifest + "\n")

    # Bind annotated tag to HEAD
    subprocess.run(["git", "tag", "-f", "-a", tag_name, "-m", manifest], check=True)
    print(f"\n[+] Applied Law of Shaped Force tag: '{tag_name}'")

if __name__ == "__main__":
    apply_law_of_shaped_force()
