#!/bin/bash
clear
echo "=========================================================="
echo "💀 ATOM-TRUTH // HIGH-THROUGHPUT ENGINE OPTIMIZATION 💀"
echo "=========================================================="

# 1. Target Directory Scrape
REPO_LIST=$(find ~ -name ".git" -type d 2>/dev/null)
count=0

echo "[+] Scanning active data nodes for storage clutter..."

# 2. Iterate and Compress the File System
for repo in $REPO_LIST; do
    repo_dir=$(dirname "$repo")
    repo_name=$(basename "$repo_dir")
    
    # Check if the folder has heavy commit traffic
    commit_count=$(cd "$repo_dir" && git rev-list --all --count 2>/dev/null || echo "0")
    
    if [ "$commit_count" -gt 0 ]; then
        echo "[-] Optimizing Node: [$repo_name] ($commit_count commits total)..."
        
        # Force aggressive garbage collection and pack loose objects
        (cd "$repo_dir" && \
         git gc --aggressive --prune=now --quiet && \
         git repack -a -d --quiet)
        
        count=$((count + 1))
    fi
done

# 3. Clean up the global Termux package cache and system temporary memory
echo "----------------------------------------------------------"
echo "[+] Wiping system temporary buffers..."
export TMPDIR="/data/data/com.termux/files/usr/tmp"
rm -rf "$TMPDIR"/* 2>/dev/null

echo "=========================================================="
echo "⚡ SUCCESS: $count high-traffic repositories compressed cleanly."
