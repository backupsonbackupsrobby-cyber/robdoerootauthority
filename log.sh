#!/bin/bash
clear

# 1. Grab your existing custom hash
HASH=$(cat .sha86400_root_token 2>/dev/null || echo "GENESIS-HASH")

# 2. Get the current date and battery
DATE_STR=$(date "+%A, %B %d, %Y at %I:%M %p")
BATT=$(cat /sys/class/power_supply/battery/capacity 2>/dev/null || echo "100")

# 3. Create the header inside your file
echo "=============================================" >> diary.txt
echo "STAMP: $HASH" >> diary.txt
echo "TIME:  $DATE_STR | BATTERY: $BATT%" >> diary.txt
echo "=============================================" >> diary.txt

# 4. Prompt you to type your entry
echo "📝 Type your note below (Press Ctrl+D when you are finished):"
echo "---------------------------------------------"

# 5. Take your input and append it to the diary
cat >> diary.txt

echo -e "\n[+] Saved to diary.txt!\n"
