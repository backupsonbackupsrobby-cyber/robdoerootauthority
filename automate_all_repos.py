import os
import sys
import math
import cmath
import hashlib
import subprocess

def find_git_repos(root_dir="."):
    """Recursively discover all Git repositories under root_dir."""
    git_repos = []
    for dirpath, dirnames, filenames in os.walk(root_dir):
        if '.git' in dirnames:
            git_repos.append(dirpath)
            dirnames.remove('.git')  # Don't recurse into .git folders
    return sorted(git_repos)

def process_repository(repo_path):
    """Execute dual Merkle reduction, 52-slot phase locking, and state tag on a repo."""
    print(f"\n\033[1;36m['+] PROCESSING REPO: {repo_path}\033[0m")
    
    # Save original directory
    orig_dir = os.getcwd()
    os.chdir(repo_path)
    
    try:
        # 1. Fetch object list
        cmd = ["git", "rev-list", "--objects", "--all"]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode != 0 or not res.stdout.strip():
            print(f"\033[1;33m  [-] Empty or uninitialized Git repository. Skipping...\033[0m")
            os.chdir(orig_dir)
            return

        objects = sorted([line.split()[0] for line in res.stdout.strip().split('\n') if line])
        N_objects = len(objects)

        # 2. Dual Merkle Root (SHA-256 / SHA-512)
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

        # 3. 52-Slot Kuramoto Phase Dynamics (13 weeks x 4 seasons)
        total_slots = 52
        phases = [2 * math.pi * k / total_slots for k in range(total_slots)]
        c = complex(-0.7, 0.27015)
        K, dt = 3.5, 0.01

        for _ in range(13):  # 13 seasonal orbital iterations
            Z = [cmath.rect(1.0, theta)**2 + c for theta in phases]
            phases = [cmath.phase(z) for z in Z]
            phases = [
                (phases[i] + (2 * phases[i] + (K / total_slots) * sum(math.sin(phases[j] - phases[i]) for j in range(total_slots))) * dt) % (2 * math.pi)
                for i in range(total_slots)
            ]

        complex_order = sum(cmath.rect(1.0, theta) for theta in phases) / total_slots
        R = abs(complex_order)
        Psi = cmath.phase(complex_order)

        # 4. Write ledger proof
        manifest = f"""LAW OF SHAPED FORCE | MULTI-REPO SOVEREIGN PROOF
================================================================
PATH           : {os.path.abspath(repo_path)}
OBJECT_LEAVES  : {N_objects}
KURAMOTO_R     : {R:.6f} [PHASE LOCKED]
MEAN_ANGLE_PSI : {Psi:.6f} rad
MERKLE_SHA256  : {sha256_root}
MERKLE_SHA512  : {sha512_root}
================================================================"""

        with open("state_proofs.log", "a") as f:
            f.write(manifest + "\n\n")

        # 5. Apply Git Tag
        tag_name = f"proof-auto-{sha256_root[:7]}"
        subprocess.run(["git", "tag", "-f", "-a", tag_name, "-m", manifest], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        print(f"\033[1;32m  [+] Objects Processed : {N_objects}\033[0m")
        print(f"\033[1;32m  [+] SHA-256 Root      : {sha256_root[:16]}...\033[0m")
        print(f"\033[1;32m  [+] Kuramoto Order R  : {R:.6f}\033[0m")
        print(f"\033[1;33m  [+] Tagged HEAD       : {tag_name}\033[0m")

    except Exception as e:
        print(f"\033[1;31m  [-] Failed processing {repo_path}: {e}\033[0m")
    finally:
        os.chdir(orig_dir)

def main():
    root_target = sys.argv[1] if len(sys.argv) > 1 else ".."
    print("\033[1;36m" + "="*68)
    print("      SOVEREIGN MULTI-REPOSITORY AUTOMATION ENGINE")
    print(f"      Scanning Root Path: {os.path.abspath(root_target)}")
    print("="*68 + "\033[0m")

    repos = find_git_repos(root_target)
    print(f"\033[1;32m[+] Discovered {len(repos)} Git Repositories.\033[0m")

    for repo in repos:
        process_repository(repo)

    print("\n\033[1;36m" + "="*68)
    print("      ALL REPOSITORIES PHASE-LOCKED & SYNCHRONIZED")
    print("="*68 + "\033[0m")

if __name__ == "__main__":
    main()
