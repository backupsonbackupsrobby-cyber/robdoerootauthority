#!/usr/bin/env python3
"""
CIRCADIAN RHYTHM PULSE EMITTER (EHF TIER 0)
Maps local time to biological clock phases and emits local telemetry.
Cadence: tau = 12s | Anchor: ko_te_mana_o_te_tangata
"""

import time
from datetime import datetime
from pathlib import Path
import json

IDENTITY_ANCHOR = "ko_te_mana_o_te_tangata"

def get_current_circadian_phase(hour):
    if 22 <= hour or hour < 2:
        return {"phase": "Deep Sleep", "cortisol": "Low", "energy": "Low", "intent": "Recovery/Healing", "freq_hz": 1.0}
    elif 2 <= hour < 6:
        return {"phase": "Light Sleep", "cortisol": "Rising", "energy": "Rising", "intent": "Preparation", "freq_hz": 2.0}
    elif 6 <= hour < 7:
        return {"phase": "Wake-Up", "cortisol": "PEAK", "energy": "Increasing", "intent": "Activation", "freq_hz": 10.0}
    elif 7 <= hour < 9:
        return {"phase": "Morning Peak", "cortisol": "High", "energy": "PEAK", "intent": "Decision-Making", "freq_hz": 10.0}
    elif 9 <= hour < 13:
        return {"phase": "Focus Window", "cortisol": "High", "energy": "Sustained", "intent": "Deep Work", "freq_hz": 6.0}
    elif 13 <= hour < 15:
        return {"phase": "Post-Lunch Dip", "cortisol": "Declining", "energy": "LOW", "intent": "Admin Tasks", "freq_hz": 10.0}
    elif 15 <= hour < 17:
        return {"phase": "Afternoon Peak", "cortisol": "Recovering", "energy": "Rising", "intent": "Execution", "freq_hz": 20.0}
    else:
        return {"phase": "Evening Wind Down", "cortisol": "Declining", "energy": "Declining", "intent": "Planning/Light", "freq_hz": 10.0}

def pulse_circadian():
    print("--- 🧬 EHF CIRCADIAN RHYTHM PULSE INITIALIZED ---")
    now = datetime.now()
    current_hour = now.hour
    
    phase_data = get_current_circadian_phase(current_hour)
    
    print(f"  [+] Local Time: {now.strftime('%H:%M:%S')}")
    print(f"  [+] Active Circadian Phase: {phase_data['phase']}")
    print(f"  [+] Cortisol Curve: {phase_data['cortisol']} | Energy Level: {phase_data['energy']}")
    print(f"  [+] Optimal Intent: {phase_data['intent']} ({phase_data['freq_hz']} Hz)")
    
    manifest = {
        "identity_anchor": IDENTITY_ANCHOR,
        "timestamp": now.isoformat(),
        "circadian_phase": phase_data
    }
    
    Path("CIRCADIAN_STATE.lock").write_text(json.dumps(manifest, indent=2), encoding='utf-8')
    print("✅ Circadian state written to local ledger. Quiet lantern is synchronized.\n")

if __name__ == "__main__":
    pulse_circadian()
