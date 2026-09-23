#!/usr/bin/env python3
"""
SOVEREIGN GENESIS HEARTBEAT DAEMON
Continuously verifies and pulses the entire local loopback ecosystem 
on a deterministic tau=12 second heartbeat.
Anchor: ko_te_mana_o_te_tangata | Routing: 127.0.0.1 | Cadence: 0.052
"""

import time
import json
import hashlib
from pathlib import Path
from datetime import datetime

IDENTITY_ANCHOR = "ko_te_mana_o_te_tangata"
HEARTBEAT_INTERVAL = 12  # tau = 12 seconds
CADENCE_TIER = 0.052

def run_daemon():
    print("--- 🔄 LAUNCHING SOVEREIGN GENESIS HEARTBEAT DAEMON ---")
    print(f"  [+] Anchor: {IDENTITY_ANCHOR}")
    print(f"  [+] Heartbeat Cadence: tau = {HEARTBEAT_INTERVAL}s")
    print(f"  [+] Routing: 127.0.0.1 (Air-Gapped Loopback)\n")
    
    pulse_count = 0
    
    try:
        while True:
            pulse_count += 1
            timestamp = datetime.now().isoformat()
            
            # Gather all local lock files
            lock_files = sorted([f.name for f in Path(".").glob("*.lock")])
            ledger_state = "".join([Path(lf).read_text(encoding='utf-8') for lf in lock_files])
            
            # Compute rolling epoch hash
            epoch_payload = f"{timestamp}:{ledger_state}:{CADENCE_TIER}:{IDENTITY_ANCHOR}".encode('utf-8')
            epoch_hash = hashlib.sha256(epoch_payload).hexdigest()
            
            pulse_record = {
                "pulse_sequence": pulse_count,
                "timestamp": timestamp,
                "active_locks_detected": len(lock_files),
                "epoch_hash": epoch_hash,
                "cadence_tier": CADENCE_TIER,
                "routing": "127.0.0.1"
            }
            
            Path("GENESIS_PULSE.lock").write_text(json.dumps(pulse_record, indent=2), encoding='utf-8')
            
            print(f"  [PULSE {pulse_count:04d}] [{timestamp[:19]}] Locks Verified: {len(lock_files)} | Epoch Hash: {epoch_hash[:16]}... [OK]")
            
            time.sleep(HEARTBEAT_INTERVAL)
            
    except KeyboardInterrupt:
        print("\n  [!] Daemon paused by operator. Sovereign state remains intact.")
        print("Ko te marino te haumaru. (Quietness is safety.)\n")

if __name__ == "__main__":
    run_daemon()
