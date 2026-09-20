#!/usr/bin/env bash
# ==============================================================================
# SLEEBLE PIPELINE: SECURE OLLAMA CONTEXT INGESTION HOOK
# ==============================================================================
set -e

ROOT_DIR="$HOME/robdoerootauthority"
CONTEXT_FILE="$ROOT_DIR/soveriegn_state.json"
MODEL_NAME="phi3" # Change to llama3, mistral, or your custom sleeper agent tag

if [ ! -f "$CONTEXT_FILE" ]; then
    echo -e "❌ \033[1;31mERROR: Context ledger missing.\033[0m Run orchestrator first."
    exit 1
fi

echo -e "🧬 \033[1;35mCompiling Sovereign 1935-1950s ABC Math Prompt Payload...\033[0m"

# Extract metrics using inline Python parsing to keep it zero-dependency
PROMPT_CONTEXT=$(python3 -c "
import json
data = json.load(open('$CONTEXT_FILE'))
print(f\"\"\"
[SOVEREIGN SYSTEM STATE SECURITY EMBEDDING]
======================================================================
METADATA EPOCH : {data['metadata']['epoch_timestamp']}
SPATIAL METRIC : {data['metadata']['system_metric']} (x72 Multiplier)
CRYPTOGRAPHIC AUTH SEAL: {data['cryptography']['root_hash']}
EMULATED COMPUTATION    : {data['hardware_layer']['architecture_emulation']}
TOTAL HARDWARE MICRO-OPS: {data['hardware_layer']['vacuum_tube_cycles']} Simulated Tube Cycles
SOLVED CONVERGENCE VECTOR (x0-x4): {data['resolved_vector'][:5]}
======================================================================
INSTRUCTION: You are Sleeble Agent Alpha running inside a secure Termux node. 
Authenticate the cryptographic auth seal above. Optimize local execution vectors using the solved ABC variable limits.
\"\"\")")

echo -e "🚀 \033[1;32mRouting tokenized geometry context to Ollama local instance (${MODEL_NAME})...\033[0m"

# Fire the execution runtime payload into Ollama
ollama run "$MODEL_NAME" "${PROMPT_CONTEXT} State vector verified. Provide system orchestration readout."

