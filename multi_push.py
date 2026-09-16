import subprocess

remotes = ["origin", "github-robby", "gods-eye-view", "ladbot"]

print("\033[1;31m===================================================\033[0m")
print("\033[1;31m  [MULTI-REMOTE SYNC] : PUSHING ACTIVE BRANCH      \033[0m")
print("\033[1;31m===================================================\033[0m")

# Fixed: extract .stdout before stripping
res_branch = subprocess.run(["git", "branch", "--show-current"], capture_output=True, text=True)
current_branch = res_branch.stdout.strip()
print(f"\n[INFO] Active local branch detected: '{current_branch}'")

for remote in remotes:
    print(f"\n\033[1;33m[SYNC] Pushing {current_branch} -> {remote}/main...\033[0m")
    try:
        res_push = subprocess.run(["git", "push", remote, f"{current_branch}:main"], capture_output=True, text=True)
        res_tags = subprocess.run(["git", "push", remote, "--tags"], capture_output=True, text=True)
        
        if res_push.returncode == 0:
            print(f"  └─ \033[1;32m[SUCCESS] Synced to {remote}\033[0m")
        else:
            print(f"  └─ \033[1;33m[NOTICE] {remote}: {res_push.stderr.strip()}\033[0m")
            
    except Exception as e:
        print(f"  └─ \033[1;31m[ERROR] Failed on {remote}: {e}\033[0m")

print("\n\033[1;31m---------------------------------------------------\033[0m")
print("\n\033[1;32m[COMPLETE]: Multi-namespace sync locked, Bruz.\033[0m")
print("\033[1;31m===================================================\033[0m\n")

