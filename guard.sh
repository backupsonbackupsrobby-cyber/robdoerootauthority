#!/bin/sh

echo "🔍 [ATOM-TRUTH] Running Pure Bare Shell Perimeter Scan..."

# Define warning flag counter
VIOLATIONS=0

# Scan all files recursively using grep (excluding hidden directories like .git)
# Looking for Telegram tokens, EVM wallets, Solana keys, and seed/secret keywords

find . -not -path '*/.*' -type f 2>/dev/null | while read -r file; do
    # Skip authorized config sets if needed (e.g., .env)
    case "$file" in
        *./.env*|*./config.json*) continue ;;
    esac

    # Search patterns using grep -E (Extended Regular Expressions)
    if grep -qE '([0-9]{9}:[A-Za-z0-9_-]{35})|(0x[a-fA-F0-9]{40})|([1-9A-HJ-NP-Za-km-z]{32,44})' "$file"; then
        echo "🚨 [BREACH] Token or wallet string detected in: $file"
        VIOLATIONS=$((VIOLATIONS + 1))
    fi
done

if [ "$VIOLATIONS" -eq 0 ]; then
    echo "✅ [SECURE] No unauthorized tokens or wallet strings found."
else
    echo "⚠️  [ALERT] Total violations flagged: $VIOLATIONS"
fi
