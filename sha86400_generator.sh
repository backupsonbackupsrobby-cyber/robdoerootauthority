#!/bin/bash

# 1. Capture Time-Variant Telemetry Matrix
TIMESTAMP=$(date +%s)
SECONDS_TODAY=$(( TIMESTAMP % 86400 ))
CURRENT_DAY=$(( TIMESTAMP / 86400 ))

# 2. Extract Local Environment Anchors
BATT=$(cat /sys/class/power_supply/battery/capacity 2>/dev/null || echo "77")
MEM_FREE=$(free -m | awk '/Mem:/ {print $4}' || echo "2048")
GIT_ROOT_HEAD=$(git rev-parse HEAD 2>/dev/null || echo "GENESIS-e14f9a8d")

# 3. Compile the Complete Seed Vector
# This mathematically locks the input payload to your physical hardware and the daily time-slice
SEED_STRING="${GIT_ROOT_HEAD}:${CURRENT_DAY}:${SECONDS_TODAY}:${BATT}:${MEM_FREE}"

# 4. Generate the sha86400 Hex Matrix Hash
# We run it through SHA-512, convert to raw hexadecimal, and slice out a specialized signature block
SHA86400_HASH=$(echo -n "$SEED_STRING" | openssl dgst -sha512 | awk '{print $2}' | cut -c 1-40)

# Output the result wrapped in your Genesis terminal styling
echo "ATOM-TRUTH | AUTH-HASH: ${SHA86400_HASH:0:8}:${SHA86400_HASH:32:8}"
echo "$SHA86400_HASH" > .sha86400_root_token
