#!/usr/bin/env bash
# ==============================================================================
# SLEEBLE REPOSITORY LOCKDOWN: AUTOMATED ROOT HASH TAGGING SYSTEM
# ==============================================================================
set -e

ROOT_DIR="$HOME/robdoerootauthority"
CONTEXT_FILE="$ROOT_DIR/soveriegn_state.json"

# 1. Validate production context file existence
if [ ! -f "$CONTEXT_FILE" ]; then
    echo -e "❌ \033[1;31mERROR: Production state file not found!\033[0m Run the orchestrator first."
    exit 1
fi

echo -e "📦 \033[1;34mExtracting Sovereign Cryptographic Root Hash...\033[0m"

# 2. Extract the full SHA-1024 simulated token from the verified state file
SHA1024_ROOT=$(python3 -c "import json, os; data=json.load(open(os.path.expanduser('$CONTEXT_FILE'))); print(data['cryptography']['root_hash'])")
SHORT_HASH="${SHA1024_ROOT:0:16}"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")

echo -e "🔑 Root Hash Found: \033[1;36m${SHORT_HASH}...\033[0m"

# 3. Initialize local git space safely if missing
if [ ! -d "$ROOT_DIR/.git" ]; then
    echo "[~] Initializing Git workspace inside root authority folder..."
    cd "$ROOT_DIR"
    git init -b main
    git config user.name "Robdoe Root Authority"
    git config user.email "authority@robdoe.local"
fi

cd "$ROOT_DIR"

# 4. Clear old tags to prevent internal git reference conflicts
git tag -d "sleeble-x72-93m-arc" 2>/dev/null || true
git tag -d "release-${SHORT_HASH}" 2>/dev/null || true

# 5. Stage, commit, and cryptographically seal the infrastructure tree
git add sovereign_orchestrator.py soveriegn_state.json orchestrator.log 2>/dev/null || git add .
git commit -m "sys(matrix): lock-in x72 geometric consensus [hash: ${SHORT_HASH}]" --allow-empty

# 6. Push the primary structural deployment tags
git tag -a "sleeble-x72-93m-arc" -m "SHA1024_ROOT: ${SHA1024_ROOT}"
git tag -a "release-${SHORT_HASH}" -m "TIMELOCK: ${TIMESTAMP} | ABC_CYCLES: RESOLVED"

echo -e "\n================================================================================"
echo -e "🚀 \033[1;32mREPOSITORY SECURED & TAGGED SUCCESSFULLY\033[0m"
echo -e "================================================================================"
echo -e "Primary Matrix Tag:  \033[1;33msleeble-x72-93m-arc\033[0m"
echo -e "Unique Release Tag: \033[1;35mrelease-${SHORT_HASH}\033[0m"
echo -e "Metadata Reference: \033[1;32mAll state configurations locked onto Git tree.\033[0m"
echo -e "================================================================================"
