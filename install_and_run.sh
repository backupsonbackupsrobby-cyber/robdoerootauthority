#!/bin/bash
set -e

# Target Setup
WORKDIR="/data/data/com.termux/files/home/robdoerootauthority"
LLAMA_DIR="$WORKDIR/llama.cpp"
MODEL_DIR="$WORKDIR/models"
MODEL_PATH="$MODEL_DIR/Llama-3.2-3B-Instruct-Q4_K_M.gguf"
THREADS=$(nproc)

clear
echo "=========================================================="
echo "💀 ATOM-TRUTH // UNIFIED HARDWARE PIPELINE INITIALISING 💀"
echo "=========================================================="

# 1. Reset broken TMPDIR setups and force native Termux memory space
export TMPDIR="/data/data/com.termux/files/usr/tmp"
mkdir -p "$TMPDIR"

# 2. Synchronize environment toolchain dependencies
echo "[+] Validating system toolchain..."
pkg update && pkg upgrade -y
pkg install git cmake clang make curl procps -y

# 3. Clean environment and pull exact target repository
cd "$WORKDIR"
if [ -d "$LLAMA_DIR" ]; then
    echo "[!] Existing directory detected. Obliterating stale data..."
    rm -rf "$LLAMA_DIR"
fi

echo "[+] Cloning official high-performance engine..."
# Hardcoded to prevent variable expansion or string truncating drops
git clone --depth 1 https://github.com "$LLAMA_DIR"

# 4. Native compilation phase
cd "$LLAMA_DIR"
echo "[+] Constructing build matrix for ARM64 architecture..."
cmake -B build -DCMAKE_BUILD_TYPE=Release -DGGML_NATIVE=OFF -DGGML_CPU=ON

echo "[+] Compiling core binaries with $THREADS threads..."
cmake --build build --config Release -j"$THREADS"

# 5. Quantized Model Allocation
mkdir -p "$MODEL_DIR"
if [ ! -f "$MODEL_PATH" ]; then
    echo "[+] Model not found. Downloading Llama-3.2-3B-Instruct (Q4_K_M)..."
    curl -L -o "$MODEL_PATH" "https://huggingface.co"
else
    echo "[+] Verified valid model matrix at $MODEL_PATH"
fi

# 6. Extract Telemetry data for Live Persona Prompt
echo "[+] Processing dynamic device context..."
BATT=$(cat /sys/class/power_supply/battery/capacity 2>/dev/null || echo "100")
MEM_FREE=$(free -m | awk '/Mem:/ {print $4}')
UPTIME=$(uptime | awk -F, '{print $1}' | awk '{print $3,$4}')

SYSTEM_PROMPT="You are a localized core AI running completely offline within an Android ARM64 architecture terminal. Operating environment telemetry: Current Battery: ${BATT}%, Free System Memory: ${MEM_FREE}MB, Host Uptime: ${UPTIME}. Your handler is a root-level operator at Robdoe.com. Be concise, lethal with your technical precision, and maintain a highly advanced, non-handholding tone."

echo "----------------------------------------------------------"
echo "💀 EXECUTING LOCAL SILICON INSTANCE 💀"
echo "----------------------------------------------------------"

# Launch inference pipeline
"$LLAMA_DIR/build/bin/llama-cli" \
    -m "$MODEL_PATH" \
    -t "$THREADS" \
    -p "<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n\n$SYSTEM_PROMPT<|eot_id|><|start_header_id|>user<|end_header_id|>\n\n" \
    -r "<|eot_id|>" \
    --in-prefix "\n<|start_header_id|>user<|end_header_id|>\n\n" \
    --in-suffix "<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\n" \
    -i \
    --color \
    -c 2048 \
    --temp 0.7 \
    --repeat_penalty 1.1
