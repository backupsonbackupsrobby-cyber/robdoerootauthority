with open("deploy_2026_matrix.py", "r") as f:
    code = f.read()

# Replace hardcoded main push with dynamic branch resolution
old_target = 'os.system("git push origin main --tags")'
new_target = 'current_branch = os.popen("git branch --show-current").read().strip()\n    os.system(f"git push origin {current_branch} --tags")'

if old_target in code:
    code = code.replace(old_target, new_target)
    with open("deploy_2026_matrix.py", "w") as f:
        f.write(code)
    print("\033[1;32m[✓] deploy_2026_matrix.py patched for dynamic branch pushing.\033[0m")
else:
    print("\033[1;33m[*] Target push string already updated or customized.\033[0m")
