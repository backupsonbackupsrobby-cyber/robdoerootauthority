import subprocess

def run_cmd(cmd):
    print(f"[EXEC] {cmd}")
    res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if res.stdout:
        print(res.stdout.strip())
    if res.stderr and res.returncode != 0:
        print(f"[STDERR] {res.stderr.strip()}")
    return res.returncode

def re_align_remote():
    print("========================================================")
    print("⚡ RE-ALIGNING TO VERIFIED BACKUPNSBACKUPS NAMESPACE ⚡")
    print("========================================================")
    
    # Point origin to the active working HTTPS remote namespace (github-robby)
    run_cmd("git remote set-url origin https://github.com/backupsonbackupsrobby-cyber/robdoerootauthority.git")
    
    print("\n[INFO] Pushing sovereign branch to verified origin...")
    status = run_cmd("git push origin main")
    
    if status == 0:
        print("[SUCCESS] Grid state successfully synchronized to GitHub.")
    else:
        print("[ERROR] Push failed. Check credentials or token configuration.")

if __name__ == "__main__":
    re_align_remote()
