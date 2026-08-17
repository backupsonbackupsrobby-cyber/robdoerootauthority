#!/usr/bin/env python3
import datetime
import subprocess

def run_cmd(cmd):
    res = subprocess.run(cmd, capture_output=True, text=True)
    return res.stdout.strip()

def main():
    print("================================================================")
    print("  KINETIC TAG WITNESS: RECORDING SYSTEM STATE & INTENT         ")
    print("================================================================")
    
    timestamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%d%H%M%S")
    tag_name = f"v2026.8.12-KINETIC-ENERGY-RECYCLE-{timestamp}"
    msg = "Kinetic energy recycle and system space state witness lock"
    
    print(f"[*] Creating witness tag: {tag_name}")
    
    # Prune first to ensure index can handle operations if space permits, or force tag creation
    subprocess.run(["git", "tag", "-f", tag_name, "-m", msg], check=False)
    subprocess.run(["git", "push", "origin", "tag", tag_name, "--force"], check=False)
    
    print(f"[+] Kinetic witness tag {tag_name} processed.")
    print("================================================================")

if __name__ == "__main__":
    main()
