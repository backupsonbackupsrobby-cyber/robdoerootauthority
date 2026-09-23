#!/data/data/com.termux/files/usr/bin/bash

# Acquire Android CPU wake-lock to prevent OS throttling
termux-wake-lock

# Path configuration
LOG_FILE="daemon.log"
SCRIPT="adaptive_node.py"

echo "[SUPERVISOR] Starting persistent node loop for $SCRIPT at $(date)" >> "$LOG_FILE"

# Supervisor restart loop
while true; do
    echo "[SUPERVISOR] Launching $SCRIPT..." >> "$LOG_FILE"
    
    # Execute python script and append output to log
    python3 "$SCRIPT" >> "$LOG_FILE" 2>&1
    
    EXIT_CODE=$?
    echo "[SUPERVISOR] Process exited with code $EXIT_CODE at $(date). Restarting in 3s..." >> "$LOG_FILE"
    
    # Short delay to prevent rapid cpu-spinning if there's a fatal syntax/import error
    sleep 3
done
