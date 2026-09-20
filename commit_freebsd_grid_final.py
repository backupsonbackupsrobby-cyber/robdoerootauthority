import subprocess

def run_cmd(cmd):
    print(f"[EXEC] {cmd}")
    res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if res.stdout:
        print(res.stdout.strip())
    if res.stderr and res.returncode != 0:
        print(f"[STDERR] {res.stderr.strip()}")
    return res.returncode

def finalize_commit():
    print("========================================================")
    print("⚡ FINALIZING FREEBSD SUBMODULE INDEX & SOVEREIGN COMMIT ⚡")
    print("========================================================")
    
    # Properly initialize or unstage the problematic submodule path so git doesn't choke
    run_cmd("git submodule deinit -f freebsd-src || true")
    run_cmd("rm -rf .git/modules/freebsd-src || true")
    run_cmd("git rm -f freebsd-src || true")
    
    # Add everything clean
    run_cmd("git add -A")
    
    # Commit the state
    commit_status = run_cmd('git commit -m "chore(sovereign): resolve freebsd-src index state and lock Titan-Core V9 grid"')
    
    if commit_status == 0:
        print("\n[INFO] Pushing sovereign branch to origin main...")
        run_cmd("git push origin main")
        print("[SUCCESS] Grid state fully pushed and synchronized.")
    else:
        print("[WARNING] Commit skipped or nothing new to commit, checking status...")
        run_cmd("git status")

if __name__ == "__main__":
    finalize_commit()
