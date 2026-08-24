#!/bin/zsh

LOG_FILE="$HOME/robdoerootauthority/auth_access.log"
LOCK_FILE="$HOME/robdoerootauthority/locks/fabtecmetalworks.lock"
BANTIME=31536000 # 1 full year in seconds (365 days)

mkdir -p "$HOME/robdoerootauthority/locks"
touch "$LOG_FILE"

echo "--- TARGET SENTINEL ONLINE: 1-YEAR HARD LOCKOUT ARMED ---"

# Tail the log file in real time
tail -Fn0 "$LOG_FILE" | while read -r line; do
    # Check if the specific target email appears in the incoming attempt or log
    if echo "$line" | grep -qi "fabtecmetalworks@yahoo.com"; then
        
        # If not already locked, apply the 1-year block state
        if [ ! -f "$LOCK_FILE" ]; then
            touch "$LOCK_FILE"
            echo "[LOCKDOWN] Target identified: fabtecmetalworks@yahoo.com. Password wiped. Locked out for 1 full year."
            
            (
                # Run background timer to auto-lift after 1 year (31536000 seconds)
                sleep $BANTIME
                rm -f "$LOCK_FILE"
                echo "[RELEASE] 1-year penalty expired for fabtecmetalworks@yahoo.com."
            ) &
        else
            echo "[BLOCKED] Hit from fabtecmetalworks@yahoo.com rejected. Serving the 1-year lockout."
        fi
    fi
done
