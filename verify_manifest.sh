#!/bin/bash
# ==============================================================================
# OPERATOR STACK: POSIX NATIVE LATTICE VERIFIER (NULL-SAFE TERMUX ONLY)
# Description: Generates a deterministic hash tree across all target proof blocks
#              using null-byte separators to safely parse quotes and whitespaces.
# ==============================================================================

set -euo pipefail

TARGET_DIR="${HOME}/robdoerootauthority"
cd "$TARGET_DIR"

echo "[*] Scanning Local Node Lattice via Safe Core Utilities..."

# 1. find -print0 outputs file paths separated by null characters (\0)
# 2. sort -z sorts the null-terminated strings deterministically
# 3. xargs -0 cleanly hands the exact paths to sha256sum without split errors
LATTICE_ROOT=$(find . -type f \( -name "*.md" -o -name "*.json" -o -name "*.jsonl" -o -name "*.sh" -o -name "*.py" \) \
    ! -path '*/.**' ! -path '*__pycache__*' ! -path '*node_modules*' -print0 | \
    sort -z | \
    xargs -0 sha256sum | \
    sha256sum | \
    awk '{print $1}')

TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

echo "=================================================="
echo "  PURE SHELL STATE SEAL: ${TIMESTAMP}"
echo "=================================================="
echo "  Lattice Root: ${LATTICE_ROOT}"
echo "=================================================="
