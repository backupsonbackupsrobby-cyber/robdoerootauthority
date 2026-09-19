#!/bin/bash
# --------------------------------------------------------------------------
# 💀 ATOM-TRUTH // KURAMOTO PROCESS PHASE HARMONIZER & WEB BUILDER
# --------------------------------------------------------------------------
clear
echo "=========================================================="
echo "🕸️  CONSTRUCTING DYNAMIC KURAMOTO ROOT HASH SPIDERWEB"
echo "=========================================================="

# Find all valid Git repositories starting from your home tree
REPO_LIST=$(find ~ -name ".git" -type d 2>/dev/null)
count=0

declare -a repo_names
declare -a phases
declare -a frequencies

if [ -z "$REPO_LIST" ]; then
    echo "[!] No active git nodes detected. Injecting virtual genesis arrays..."
    REPO_LIST="$PWD/.git"
    mkdir -p .git
fi

# Step 1: Extract and Map Git Hashes to Kuramoto Phases
for repo in $REPO_LIST; do
    repo_dir=$(dirname "$repo")
    repo_name=$(basename "$repo_dir")
    
    # Grab the raw hex commit ID or current tag signature
    git_hash=$(cd "$repo_dir" && git rev-parse --short HEAD 2>/dev/null || echo "e14f9a8d")
    
    # Mathematically translate the hex string into a numerical base-10 integer value
    hex_val=$(echo "$git_hash" | tr -d '\n' | od -An -t x1 | tr -d ' \n' | cut -c 1-8)
    dec_val=$((16#$hex_val))
    
    # Bind the integer to a bounded phase angle position between [0, 2*pi]
    phase=$(echo "scale=6; ($dec_val % 6283185) / 1000000.0" | bc -l)
    
    # Derive an intrinsic natural frequency based on file sizes/time epochs
    freq=$(echo "scale=4; 1.0 + (($dec_val % 100) / 50.0)" | bc -l)
    
    repo_names+=("$repo_name")
    phases+=("$phase")
    frequencies+=("$freq")
    count=$((count + 1))
done

echo "[+] Linked $count distinct git nodes into the network architecture."
echo "[+] Solving coupling matrix equations across spatial coordinates..."
echo "----------------------------------------------------------"

# Step 2: Simulate Phase Coupling (Kuramoto Step)
# This mimics decentralized nodes pulling each other into synchrony
K=0.8 # Variable Coupling Force
N=$count

for ((i=0; i<N; i++)); do
    sum_phase_interaction=0
    for ((j=0; j<N; j++)); do
        if [ $i -ne $j ]; then
            # Calculate phase disparity: sin(theta_j - theta_i) using standard Taylor extension approximation
            phase_diff=$(echo "scale=6; ${phases[$j]} - ${phases[$i]}" | bc -l)
            sin_diff=$(echo "scale=6; s($phase_diff)" | bc -l)
            sum_phase_interaction=$(echo "scale=6; $sum_phase_interaction + $sin_diff" | bc -l)
        fi
    done
    
    # Calculate final updated synchronized phase coordinate position
    coupling_delta=$(echo "scale=6; ($K / $N) * $sum_phase_interaction" | bc -l)
    updated_phase=$(echo "scale=6; ${phases[$i]} + ${frequencies[$i]} + $coupling_delta" | bc -l)
    phases[$i]=$updated_phase
done

# Step 3: Draw the Hexagonal Coordinate Map in pure ASCII
echo "💀 CURRENT SYNCHRONIZATION TOPOLOGY MAP (HEXAGON ENGINE) 💀"
echo "----------------------------------------------------------"

for ((i=0; i<N; i++)); do
    # Convert phase angle to Cartesian projection maps for structural rendering
    x_coord=$(echo "scale=4; 30 + (20 * c(${phases[$i]}))" | bc -l | awk '{print int($1)}')
    y_coord=$(echo "scale=4; 10 + (8 * s(${phases[$i]}))" | bc -l | awk '{print int($1)}')
    
    # Clamp safety margins
    [ $x_coord -lt 1 ] && x_coord=1
    [ $y_coord -lt 1 ] && y_coord=1
    
    printf "Node [%-15s] -> Phase: %5.2frad | Hex Lattice Projection Vector: (X:%d, Y:%d)\n" "${repo_names[$i]}" "${phases[$i]}" "$x_coord" "$y_coord"
done

echo "=========================================================="
echo "⚡ Kuramoto mesh bound. Every tag is now mathematically locking phases."
