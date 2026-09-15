import subprocess
import hashlib
import math
import cmath
import sys

def get_git_objects():
    """Retrieve all Git object hashes from the local database."""
    cmd = ["git", "rev-list", "--objects", "--all"]
    res = subprocess.run(cmd, capture_output=True, text=True, check=True)
    objects = sorted([line.split()[0] for line in res.stdout.strip().split('\n') if line])
    return objects

def compute_merkle_root(leaf_hashes, algo="sha256"):
    """Compute deterministic binary Merkle tree root using pure math layer reduction."""
    if not leaf_hashes:
        return ""
    
    current_layer = [h.encode('utf-8') for h in leaf_hashes]
    
    while len(current_layer) > 1:
        if len(current_layer) % 2 != 0:
            current_layer.append(current_layer[-1])  # Duplicate last node if odd
            
        next_layer = []
        for i in range(0, len(current_layer), 2):
            combined = current_layer[i] + current_layer[i+1]
            if algo == "sha256":
                digest = hashlib.sha256(combined).hexdigest().encode('utf-8')
            elif algo == "sha512":
                digest = hashlib.sha512(combined).hexdigest().encode('utf-8')
            next_layer.append(digest)
        current_layer = next_layer
        
    return current_layer[0].decode('utf-8')

def compute_kuramoto_order_parameter(object_hashes):
    """Map object hex values to unit circle phases [0, 2pi) and compute order parameter r."""
    N = len(object_hashes)
    if N == 0:
        return 0.0
    
    phases = []
    for h in object_hashes:
        # Convert first 8 hex chars to integer normalized to [0, 2*pi)
        val = int(h[:8], 16)
        phase = (val / 0xFFFFFFFF) * 2 * math.pi
        phases.append(phase)
        
    complex_sum = sum(cmath.exp(1j * theta) for theta in phases) / N
    return abs(complex_sum)

def main():
    objects = get_git_objects()
    N = len(objects)
    
    print(f"[+] Total Git Objects Indexed: {N}")
    
    sha256_root = compute_merkle_root(objects, "sha256")
    sha512_root = compute_merkle_root(objects, "sha512")
    r_param = compute_kuramoto_order_parameter(objects)
    
    tag_name = f"proof-{sha256_root[:7]}"
    
    tag_message = f"""SOVEREIGN MERKLE STATE PROOF
================================================================
OBJECT_COUNT   : {N}
KURAMOTO_R     : {r_param:.6f}
MERKLE_SHA256  : {sha256_root}
MERKLE_SHA512  : {sha512_root}
================================================================"""

    print("\n" + tag_message)
    
    # Save to local text artifact
    with open("merkle_hex_vomit.txt", "w") as f:
        f.write(tag_message + "\n")
        
    # Apply annotated Git tag bound to the pure math state
    subprocess.run(["git", "tag", "-f", "-a", tag_name, "-m", tag_message], check=True)
    print(f"\n[+] Successfully tagged current HEAD as '{tag_name}'")

if __name__ == "__main__":
    main()
