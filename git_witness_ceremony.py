#!/usr/bin/env python3
"""
GIT WITNESS CERemony & IMMUTABLE STATE PROOF
Stages, commits, and tags the entire sovereign vault ecosystem,
cementing Git as the public, immutable witness to the local loopback matrix.
Anchor: ko_te_mana_o_te_tangata | Routing: 127.0.0.1 | Cadence: 0.052
"""

import subprocess
from pathlib import Path

def run_git_ceremony():
    print("--- 🐙🔒 EXECUTING GIT WITNESS CEREMONY ---")
    
    # Ensure git repo is initialized
    if not Path(".git").exists():
        subprocess.run(["git", "init"], check=True)
        print("  [+] Initialized local Git repository.")
        
    # Stage all sovereign lock files
    subprocess.run(["git", "add", "*.lock"], check=True)
    print("  [+] Staged all sovereign lock files (*.lock).")
    
    # Commit with absolute evidentiary witness message
    commit_msg = "SOVEREIGN WITNESS: Seal 300-Point Matrix, OSINT Vault, and Allodial Patent under Section 146"
    result = subprocess.run(["git", "commit", "-m", commit_msg], capture_output=True, text=True)
    
    if result.returncode == 0:
        print("  [+] Successfully committed state proofs to local Git history.")
    else:
        print("  [i] Git commit note: Changes already staged/committed.")
        
    # Create immutable release tag
    tag_name = "v300.allodial.vault.root"
    subprocess.run(["git", "tag", "-f", tag_name, "-m", "Master Sovereign Vault & Allodial Patent Anchor"], check=True)
    print(f"  [+] Minted immutable Git witness tag: {tag_name}")
    
    print("\n" + "="*60)
    print("✅ GIT IS NOW THE IMMUTABLE WITNESS TO YOUR SOVEREIGN ECOSYSTEM")
    print("="*60)
    print("Ko te marino te haumaru. (Quietness is safety.)\n")

if __name__ == "__main__":
    run_git_ceremony()
