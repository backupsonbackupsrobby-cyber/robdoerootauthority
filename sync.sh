#!/bin/bash
set -euo pipefail

TARGET_DIR="${HOME}/robdoerootauthority"
REMOTE_NAME="github-robby"
BRANCH_NAME="main"
LOG_FILE="${TARGET_DIR}/.operator_sync.log"

echo "[*] Launching Node Sync Logic..." | tee -a "$LOG_FILE"

if [ ! -d "$TARGET_DIR" ]; then
    mkdir -p "$TARGET_DIR"
fi

cd "$TARGET_DIR"

if [ ! -d ".git" ]; then
    echo "[!] Path is not an initialized workspace."
    exit 1
fi

echo "[*] Synchronizing with remote reference [${REMOTE_NAME}]..."
git fetch "$REMOTE_NAME" 2>>"$LOG_FILE" || echo "[!] Remote [${REMOTE_NAME}] unreachable, proceeding with local staging."

git add -A

if ! git diff-index --quiet HEAD --; then
    TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
    COMMIT_MSG="node-sync: delta update at ${TIMESTAMP}"
    echo "[+] Uncommitted variations detected. Finalizing block..."
    git commit -m "$COMMIT_MSG" >> "$LOG_FILE"
    echo "[+] Staged changes recorded: $COMMIT_MSG"
else
    echo "[+] Local tree matches latest index. No variations to record."
fi

if git ls-remote --exit-code "$REMOTE_NAME" &> /dev/null; then
    echo "[*] Transmitting block updates upstream to ${REMOTE_NAME}..."
    git push "$REMOTE_NAME" "$BRANCH_NAME" >> "$LOG_FILE" 2>&1
    echo "[+] Sync sequence completed successfully."
else
    echo "[!] Remote peer [${REMOTE_NAME}] disconnected or offline. Block stored locally."
fi
