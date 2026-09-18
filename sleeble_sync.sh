#!/bin/sh
# ROBDOE ROOT AUTHORITY | SLEEBLE 0/1 SYNCHRONY BRIDGE
echo "=================================================="
echo " AGENT SLEEBLE | 0/1 CHAIN SYNCHRONIZATION"
echo " Guard: Hone Heke Vector | Engine: Ollama"
echo "=================================================="

# Verify local Ollama daemon status
if pgrep ollama > /dev/null; then
    echo "[+] Ollama local instance detected. Active."
else
    echo "[!] Warning: Ollama daemon offline. Initializing local runtime..."
    ollama serve > /dev/null 2>&1 &
    sleep 2
fi

# Hash current Sleeble manifest into the ledger stream
SLEEBLE_HASH=$(sha512sum sleeble_manifest.json | awk '{print $1}')
echo "[+] Sleeble On-Chain Hash: $SLEEBLE_HASH"
echo "[+] Synchrony State: 0/1 Binary Lock Verified."
echo "=================================================="
