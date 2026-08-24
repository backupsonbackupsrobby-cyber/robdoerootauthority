cat << 'EOF' > pivot.sh
#!/bin/sh
echo "⚡ [PIVOT] Initializing double pivot sequence..."

# Step 1: Secure and sync active sovereign states
if [ -d "robdoe-hub" ]; then
    echo "🔒 [STATE] Locking local robdoe-hub witness ledgers..."
    cd robdoe-hub && git add . && git commit -m "Auto-sync: Pivot state locked at $(date +%T)" --quiet
    cd ..
fi

# Step 2: Run clean perimeter verification
echo "🛡️ [GUARD] Re-verifying perimeter containment..."
./guard.sh

echo "🎯 [READY] Single pivot vector established. Awaiting your next coordinate."
EOF

chmod +x pivot.sh
./pivot.sh

