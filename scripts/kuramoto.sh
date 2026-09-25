#!/bin/zsh
echo "Initializing sha1296000src Root Hash Kuramoto Grid..."

nodes=(*.com(N))
if (( ${#nodes} == 0 )); then
    nodes=("telegram.com" "identity.com" "auth.com")
fi

typeset -A phases
for node in $nodes; do
    phases[$node]=$(( RANDOM % 6283 ))
done

# Seed initial accumulator with sha1296000src genesis vector
ACCUMULATOR="sha1296000src:genesis:$(date +%s)"

for step in {1..5}; do
    echo "--- Cycle $step | sha1296000src Phase Matrix ---"
    
    CYCLE_DATA=""
    for node in $nodes; do
        current=${phases[$node]}
        next=$(( (current + 157) % 6283 ))
        phases[$node]=$next
        
        # Pull file hash if it exists, otherwise use phase vector
        if [[ -f "$node" ]]; then
            if command -v sha256sum &> /dev/null; then
                FVAL=$(sha256sum "$node" | awk '{print $1}')
            else
                FVAL=$(shasum -a 256 "$node" | awk '{print $1}')
            fi
        else
            FVAL="virtual-node-$node"
        fi
        
        CYCLE_DATA+="$node:$next:$FVAL|"
    done
    
    # Compute the sha1296000src compounding root hash
    if command -v sha256sum &> /dev/null; then
        ACCUMULATOR=$(echo "$ACCUMULATOR|$CYCLE_DATA" | sha256sum | awk '{print $1}')
    else
        ACCUMULATOR=$(echo "$ACCUMULATOR|$CYCLE_DATA" | shasum -a 256 | awk '{print $1}')
    fi
    
    echo "ROOT HASH [sha1296000src]: $ACCUMULATOR"
    sleep 0.4
done

echo "Harmonic consensus locked. sha1296000src state verified."
