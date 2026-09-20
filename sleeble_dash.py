#!/usr/bin/env python3
"""
Sovereign Console Interface v3.0 (Elite Module)
ASCII Telemetry Dashboard & Ollama Prompt Context Generator
"""

import os
import sys
import json
import time
from pathlib import Path

ROOT_DIR = Path("~/robdoerootauthority").expanduser()
STATE_FILE = ROOT_DIR / "soveriegn_state.json"

def clear_screen():
    # True terminal ANSI clearing sequence
    print("\033[H\033[J", end="")

def read_state():
    if not STATE_FILE.exists():
        return None
    try:
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return None

def build_ollama_payload(state):
    """Generates the absolute context string to drop into your Ollama prompt."""
    meta = state.get("metadata", {})
    crypto = state.get("cryptography", {})
    hw = state.get("hardware_layer", {})
    vec = state.get("resolved_vector", [])
    
    context_block = (
        f"[SYSTEM_STATE_SEAL]\n"
        f"EPOCH: {meta.get('epoch_timestamp')}\n"
        f"METRIC: {meta.get('system_metric')} (x72 Multiplier)\n"
        f"HASH_ROOT: {crypto.get('root_hash')}\n"
        f"ABC_HARDWARE: {hw.get('architecture_emulation')}\n"
        f"TUBE_CYCLES: {hw.get('vacuum_tube_cycles')} Ops Simulated\n"
        f"RESOLVED_VECTOR_HEAD: {vec[:3]}\n"
        f"[AUTHORIZATION_STATUS: LOCKED_VALID]"
    )
    return context_block

def run_dashboard():
    try:
        while True:
            state = read_state()
            clear_screen()
            
            print("\033[1;32m┌──────────────────────────────────────────────────────────────────────────┐\033[0m")
            print("\033[1;32m│  ⚡ SLEEBLE SOVEREIGN MATRIX ENGINE ── TERMINAL TELEMETRY DASHBOARD ⚡  │\033[0m")
            print("\033[1;32m└──────────────────────────────────────────────────────────────────────────┘\033[0m")
            
            if not state:
                print(" \033[1;31m[!] Awaiting data... Ensure sovereign_orchestrator.py is active.\033[0m")
            else:
                meta = state.get("metadata", {})
                crypto = state.get("cryptography", {})
                hw = state.get("hardware_layer", {})
                vec = state.get("resolved_vector", [])
                
                # --- Row 1: System Identification ---
                print(f" \033[1;34m[SYSTEM MODE]\033[0m  {meta.get('mode').upper()} | v{state.get('version')}")
                print(f" \033[1;34m[RESOLUTION]\033[0m   {meta.get('system_metric')} Rings")
                print(f" \033[1;34m[TIMESTAMP]\033[0m    {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(meta.get('epoch_timestamp')))}")
                print("\033[1;30m ──────────────────────────────────────────────────────────────────────────\033[0m")
                
                # --- Row 2: Cryptographic Infrastructure ---
                root_hash = crypto.get("root_hash", "")
                print(f" \033[1;33m[GIT ROOTH_SH]\033[0m  {root_hash[:32]}...")
                print(f"                {root_hash[32:64]}...")
                print("\033[1;30m ──────────────────────────────────────────────────────────────────────────\033[0m")
                
                # --- Row 3: Mid-Century Hardware Acceleration ---
                print(f" \033[1;35m[ABC ENGINE]\033[0m   {hw.get('architecture_emulation')}")
                print(f" \033[1;35m[VARIABLES]\033[0m    Simultaneous Linear Systems Solved: {hw.get('variables_solved')}")
                
                # Dynamic visual vacuum tube load bar
                cycles = hw.get("vacuum_tube_cycles", 0)
                bar_length = min(20, int(cycles / 650))
                load_bar = "█" * bar_length + "░" * (20 - bar_length)
                print(f" \033[1;35m[TUBE STACK]\033[0m   [{load_bar}] {cycles} Micro-Ops Simulated")
                print("\033[1;30m ──────────────────────────────────────────────────────────────────────────\033[0m")
                
                # --- Row 4: Vector Resolution Spaces ---
                print(" \033[1;36m[STATE VECTOR RESOLUTION (FIRST 5 VARIABLES)]:\033[0m")
                for idx, val in enumerate(vec[:5]):
                    print(f"   └── Variable x{idx:02d} ──► [\033[1;37m{val:10.6f}\033[0m]")
                print("\033[1;30m ──────────────────────────────────────────────────────────────────────────\033[0m")
                
                # --- Row 5: Actionable Ollama Hook Reference ---
                print(" \033[1;32m[OLLAMA CONTEXT INGESTION PAYLOAD GENERATED]:\033[0m")
                payload_snippet = build_ollama_payload(state).replace('\n', ' | ')[:70]
                print(f"   \033[1;30m{payload_snippet}...\033[0m")
                
            print("\033[1;30m\n [Ctrl+C] to drop back to shell loop.\033[0m")
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n\033[1;33m[!] Dashboard detached cleanly from active workspace matrix.\033[0m")

if __name__ == "__main__":
    run_dashboard()
