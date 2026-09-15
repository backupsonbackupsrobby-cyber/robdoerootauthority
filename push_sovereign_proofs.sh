#!/usr/bin/env zsh
echo "[+] Pushing non-destructive sovereign tags and refs..."
git push --tags github-robby --follow-tags
git push --tags github-ladbot --follow-tags
