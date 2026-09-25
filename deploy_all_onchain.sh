#!/bin/bash
echo "[*] Initializing complete on-chain deployment of all ERC-721 assets..."
echo "[+] Authority: ATOM-TRUTH | RobDoe Pty Ltd"

if [ ! -d "node_modules" ]; then
    echo "[*] Installing Hardhat & OpenZeppelin dependencies..."
    npm install --save-dev hardhat @openzeppelin/contracts ethers
fi

echo "[*] Deploying SovereignOmniRegistry contract..."
npx hardhat run scripts/deploy_omni.js --network localhost

echo "[*] Step 1 Complete. Check your deployed contract address above."
echo "[*] To mint Chunk 1 (5,000 Bundle), run:"
echo "    npx hardhat run scripts/chunks/deploy_chunk_1.js --network localhost"
echo "[*] To mint Chunk 2 (Solo Remainder), update the address in the script and run:"
echo "    npx hardhat run scripts/chunks/deploy_chunk_2_solo.js --network localhost"
echo "=================================================="
echo "   READY TO PUSH EMPIRE ON-CHAIN"
echo "=================================================="
