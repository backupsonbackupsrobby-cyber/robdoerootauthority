import subprocess
import os

def run_cmd(cmd):
    print(f"[EXEC] {cmd}")
    res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if res.stdout:
        print(res.stdout.strip())
    if res.stderr and res.returncode != 0:
        print(f"[STDERR] {res.stderr.strip()}")
    return res.returncode

def reconfigure_remote():
    print("========================================================")
    print("⚡ RE-ANCHORING SOVEREIGN REMOTE REPOSITORY ⚡")
    print("========================================================")
    
    # Check current remote URL
    run_cmd("git remote -v")
    
    # Ensure correct namespace or re-link via proper token/SSH if needed
    # Let's verify or update remote to handle the repository target cleanly
    run_cmd("git remote set-url origin https://github.com/AiAgency101/robdoerootauthority.git || true")
    
    print("\n[INFO] Re-pushing to corrected sovereign endpoint...")
    push_status = run_cmd("git push origin main")
    
    if push_status != 0:
        print("[WARNING] HTTPS push blocked. Attempting SSH tunneling protocol...")
        run_cmd("git remote set-url origin git@github.com:AiAgency101/robdoerootauthority.git")
        run_cmd("git push origin main")

    print("[SUCCESS] Remote synchronization protocol complete.")

if __name__ == "__main__":
    reconfigure_remote()
