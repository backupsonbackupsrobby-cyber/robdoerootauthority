#!/bin/zsh
TARGET_DIR="."
LOG_FILE="$TARGET_DIR/daemon-heartbeat.log"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] DAEMON INITIALIZED: Monitoring $TARGET_DIR for state shifts..."

while true; do
    TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
    for file in *.com*(N); do
        if [[ -f "$file" ]]; then
            if command -v sha256sum &> /dev/null; then
                HASH=$(sha256sum "$file" | awk '{print $1}')
            else
                HASH=$(shasum -a 256 "$file" | awk '{print $1}')
            fi
            echo "[$TIMESTAMP] NODE: $file | HASH: $HASH" >> "$LOG_FILE"
        fi
    done
    sleep 10
done
