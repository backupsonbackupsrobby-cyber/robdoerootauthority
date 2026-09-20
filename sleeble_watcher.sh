#!/usr/bin/env bash
# ==============================================================================
# SLEEBLE DAEMON LISTENER: LIVE STATE-TRIGGERED OLLAMA PIPELINE
# ==============================================================================

TARGET_FILE="$HOME/robdoerootauthority/soveriegn_state.json"
INGEST_SCRIPT="$HOME/robdoerootauthority/ollama_ingest.sh"

echo -e "📡 \033[1;35mSLEEBLE AUTO-TRIGGER ACTIVE\033[0m"
echo "Monitoring workspace for state vector modifications..."

# Get initial file timestamp
if [ -f "$TARGET_FILE" ]; then
    LAST_MOD=$(stat -c %Y "$TARGET_FILE")
else
    LAST_MOD=0
fi

while true; do
    if [ -f "$TARGET_FILE" ]; then
        CURRENT_MOD=$(stat -c %Y "$TARGET_FILE")
        
        # Trigger execution only if the file was modified since the last check
        if [ "$CURRENT_MOD" -ne "$LAST_MOD" ]; then
            echo -e "\n⚡ \033[1;32m[DETECTED] State modification captured inside root authority folder!\033[0m"
            LAST_MOD=$CURRENT_MOD
            
            # Fire the active ingestion script
            if [ -x "$INGEST_SCRIPT" ]; then
                "$INGEST_SCRIPT"
            else
                echo "❌ Error: Ingestion hook script missing or not executable."
            fi
        fi
    fi
    sleep 1
done
