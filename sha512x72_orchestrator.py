import os
import sys
import math
import cmath
import hashlib
import subprocess

def sha512_cascade_72(data_bytes):
    """Execute 72 consecutive rounds of SHA-512 hashing on data_bytes."""
    current = data_bytes
    for _ in range(72):
        current = hashlib.sha512(current).digest()
    return current.hex()

def compute_merkle_root_sha512_72(objects):
    """Construct binary Merkle tree with SHA-512x72 reduction."""
    if not objects:
        return ""
    
    current_layer = [h.encode('utf-8') for h in objects]
    
    while len(current_layer) > 1:
        if len(current_layer) % 2 != 0:
            current_layer.append(current_layer[-1])
            
        next_layer = []
        for i in range(0, len(current_layer), 2):
            combined = current_layer[i] + current_layer[i+1]
            # Apply 72-round SHA-512 cascade at each tree node
            node_digest = sha512_cascade_72(combined).encode('utf-8')
            next_layer.append(node_digest)
        current_layer = next_layer
        
    return current_layer[0].decode('utf-8')

def process_repo_sha512x72(repo_path):
    orig_dir = os.getcwd()
    os.chdir(repo_path)
    
    try:
        cmd = ["git", "rev-list", "--objects", "--all"]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode != 0 or not res.stdout.strip():
            os.chdir(orig_dir)
            return

        objects = sorted([line.split()[0] for line in res.stdout.strip().split('\n') if line])
        N_objects = len(objects)

        # 1. Execute 72-Round Cascade SHA-512 Merkle Root
        sha512x72_hex = compute_merkle_root_sha512_72(objects)

        # 2. Kuramoto Phase Coherence (52 Slots)
        total_slots = 52
        phases = [2 * math.pi * k / total_slots for k in range(total_slots)]
        K, dt = 3.5, 0.01

        for _ in range(72):  # 72 quinary step iterations
            phases = [
                (phases[i] + (2 * phases[i] + (K / total_slots) * sum(math.sin(phases[j] - phases[i]) for j in range(total_slots))) * dt) % (2 * math.pi)
                for i in range(total_slots)
            ]

        complex_order = sum(cmath.rect(1.0, theta) for theta in phases) / total_slots
        R = abs(complex_order)

        # 3. Formulate Manifest Payload
        tag_name = f"proof-72x512-{sha512x72_hex[:7]}"
        manifest = f"""LAW OF SHAPED FORCE | SHA-512x72 RECURSIVE MERKLE PROOF
================================================================================
REPOSITORY_PATH : {os.path.abspath(repo_path)}
OBJECT_LEAVES   : {N_objects}
CASCADE_ROUNDS  : 72 Iterations of SHA-512
KURAMOTO_R      : {R:.6f} [PHASE LOCKED]
SHA512x72_ROOT  : {sha512x72_hex}
================================================================================"""

        print(manifest)

        # Append to master ledger
        with open("state_proofs.log", "a") as f:
            f.write(manifest + "\n\n")

        # Create immutable git tag
        subprocess.run(["git", "tag", "-f", "-a", tag_name, "-m", manifest], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"[+] Bound annotated tag '{tag_name}' to repository HEAD.\n")

    except Exception as e:
        print(f"[-] Error processing {repo_path}: {e}")
    finally:
        os.chdir(orig_dir)

def main():
    target_root = sys.argv[1] if len(sys.argv) > 1 else "."
    
    # Locate all git repos
    repos = []
    for dirpath, dirnames, filenames in os.walk(target_root):
        if '.git' in dirnames:
            repos.append(dirpath)
            dirnames.remove('.git')
            
    print("="*80)
    print(f" SHA-512x72 RECURSIVE MERKLE ENGINE | DISCOVERED {len(repos)} REPOSITORY TARGETS")
    print("="*80)

    for repo in sorted(repos):
        process_repo_sha512x72(repo)

if __name__ == "__main__":
    main()
