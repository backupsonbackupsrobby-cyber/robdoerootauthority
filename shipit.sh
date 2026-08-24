#!/bin/zsh
echo "[*] Staging all local changes..."
git add -A

echo "[*] Committing workspace snapshot..."
git commit -m "feat(termux-usb): native libusb file-descriptor stream harness operational for ESP32-C6 (303a:1001)"

echo "[*] Tagging build release..."
git tag -a v1.0.0-c6-native -m "Stable raw USB-Serial stream via termux-usb and libusb wrapper"

echo "[*] Pushing current branch and tags upstream..."
git push origin HEAD --tags
echo "[*] Locked in, tagged, and pushed, bruz."
