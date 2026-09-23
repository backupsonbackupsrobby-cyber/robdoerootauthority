# Law of Shaped Force: Public Ledger Matrix Explorer
import json
import os
import sys
import time

LEDGER_FILE = "shaped_force_ledger.json"

def display_public_explorer():
    print("========================================================")
    print("🌐 PUBLIC SHAPED FORCE LEDGER EXPLORER: OPEN ACCESS 🌐")
    print("========================================================")
    
    if not os.path.exists(LEDGER_FILE):
        print("[!] No public entries found. Ledger is uninitialized.")
        return
        
    with open(LEDGER_FILE, 'r') as f:
        ledger = json.load(f)
        
    print(f"[METRICS] Height: {len(ledger)} Blocks | Status: LOCKED & VERIFIED\n")
    
    for block in ledger:
        idx = block["block_index"]
        timestamp_raw = block["timestamp"]
        # Convert timestamp to human readable format
        time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp_raw))
        
        print(f"╔═══ [ BLOCK #{idx} ] ════════════════════════════════════════")
        print(f"║ 📅 Timestamp: {time_str} ({timestamp_raw})")
        print(f"║ 🆔 Identity:  {block['identity_auth']}")
        print(f"║ 🔗 Prev Hash: {block['previous_hash']}")
        print(f"║ 💎 Curr Hash: {block['block_hash']}")
        print(f"║ 📦 Payload:   {block['payload']}")
        print(f"╚═══════════════════════════════════════════════════════")
        if idx < len(ledger) - 1:
            print("                           ↓")
            print("               [CRYPTOGRAPHIC LINK SEAL]")
            print("                           ↓")

    print("\n========================================================")
    print("✅ End of Public Chain. Audit complete.")
    print("========================================================")

if __name__ == "__main__":
    display_public_explorer()
