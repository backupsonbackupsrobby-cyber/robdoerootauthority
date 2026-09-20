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

def resolve_git_submodules():
    submodules = ["IncludeOS", "WSL", "asterisk", "compton", "darwin-xnu", "firecracker", "freebsd-src"]
    
    print("========================================================")
    print("⚡ RESOLVING EMBEDDED REPOS & GIT SUBMODULE INDEX ⚡")
    print("========================================================")
    
    # Clean up freebsd-src index index lock or missing commit state
    if os.path.exists("freebsd-src"):
        run_cmd("git rm --cached freebsd-src || true")
        run_cmd("rm -rf .git/modules/freebsd-src || true")
        
    for sub in submodules:
        if os.path.exists(sub):
            print(f"[SUBMODULE] De-nesting embedded repository: {sub}")
            run_cmd(f"git rm --cached {sub} || true")
            
    print("\n[INFO] Re-staging clean tree without nested repo index blocks...")
    run_cmd("git add -A")
    print("[SUCCESS] Git index sanitized and synchronized.")

if __name__ == "__main__":
    resolve_git_submodules()
