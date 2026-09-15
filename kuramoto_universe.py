import os
import glob
import subprocess
import hashlib
import numpy as np

def find_all_git_repos(base_dir):
    """Scan directory structure for all local Git repositories and forks."""
    repos = []
    for root, dirs, files in os.walk(base_dir):
        if '.git' in dirs:
            repos.append(root)
    return repos

def get_repo_objects(repo_path):
    """Extract unique SHA objects from a specific repository."""
    try:
        cmd = ["git", "-C", repo_path, "rev-list", "--all", "--objects"]
        output = subprocess.check_output(cmd, stderr=subprocess.DEVNULL).decode().strip()
        lines = output.split('\n')
        return [l.split()[0] for l in lines if l]
    except Exception:
        return []

def main():
    home_dir = os.path.expanduser("~")
    print("\033[1;36m================================================================\033[0m")
    print("\033[1;36m   UNIVERSAL MULTI-REPO KURAMOTO COUPLING ENGINE               \033[0m")
    print("\033[1;36m================================================================\033[0m")
    
    repos = find_all_git_repos(home_dir)
    print(f"\033[1;32m[+] Discovered Repositories & Forks : {len(repos)}\033[0m")
    
    all_objects = []
    repo_breakdown = {}
    
    for r in repos:
        r_name = os.path.basename(r)
        objs = get_repo_objects(r)
        repo_breakdown[r_name] = len(objs)
        all_objects.extend(objs)
        print(f"    - Node: {r_name:<30} | Leaves: {len(objs)}")
        
    N_total = len(all_objects)
    print(f"\033[1;33m[+] Global Combined Leaf Nodes      : {N_total}\033[0m")
    print("\033[1;36m----------------------------------------------------------------\033[0m")

    if N_total == 0:
        print("[-] No Git objects found across repositories.")
        return

    # Map all global objects to phase space via SHA-512
    h_vals = [hashlib.sha512(o.encode()).digest() for o in all_objects]
    theta = np.array([(int.from_bytes(h[:4], 'big') / (2**32-1)) * 2 * np.pi for h in h_vals])
    omega = np.array([0.5 + (int.from_bytes(h[4:8], 'big') / (2**32-1)) for h in h_vals])

    K_global = 3.0
    dt = 0.05

    for t in range(10):
        Z = np.mean(np.exp(1j * theta))
        R = np.abs(Z)
        psi = np.angle(Z)
        print(f"Step {t+1:02d} | Global Nodes: {N_total} | Order Parameter R = {R:.6f} | Phase Psi = {psi:.4f} rad")
        theta = (theta + (omega + K_global * R * np.sin(psi - theta)) * dt) % (2 * np.pi)

    print("\033[1;36m================================================================\033[0m")
    print(f"\033[1;32m[+] UNIVERSAL COHERENCE LOCK: R = {R:.6f}\033[0m")
    print("\033[1;36m================================================================\033[0m")

if __name__ == "__main__":
    main()
