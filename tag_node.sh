#!/bin/bash
set -euo pipefail

TARGET_DIR="${HOME}/robdoerootauthority"
cd "$TARGET_DIR"

# 1. Ensure the repo has at least one commit
if ! git rev-parse --verify HEAD &>/dev/null; then
    echo "[!] No commits found. Run your 'save' alias first."
    exit 1
fi

# 2. Generate an absolute cryptographic reference
LAST_COMMIT=$(git rev-parse HEAD)
TIMESTAMP=$(date -u +"%Y-%m-%d-%H%M%SZ")

# 3. Compute a unique SHA-256 block hash for this specific moment
ROOT_HASH_TAG=$(echo "${LAST_COMMIT}-${TIMESTAMP}" | sha256sum | awk '{print $1}')

echo "=================================================="
echo "  NODE CRYPTO GENERATION: $(date)"
echo "=================================================="
echo "Commit Ref: $LAST_COMMIT"
echo "Hash Tag:   $ROOT_HASH_TAG"

# 4. Apply the immutable tag to the local tree
git tag -a "block-${TIMESTAMP}" -m "ROOT_HASH=${ROOT_HASH_TAG}"
echo "[+] Cryptographic tag successfully bound to history."
