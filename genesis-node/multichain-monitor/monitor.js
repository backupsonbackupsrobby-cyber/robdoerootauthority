const { ethers } = require("ethers");

// Configure target RPC endpoints for each target network
const CHAINS = [
    { name: "Ethereum Mainnet", rpc: "https://rpc.ankr.com/eth" },
    { name: "Arbitrum One",     rpc: "https://rpc.ankr.com/arbitrum" },
    { name: "Optimism",         rpc: "https://rpc.ankr.com/optimism" },
    { name: "Polygon Mainnet",  rpc: "https://rpc.ankr.com/polygon" },
    { name: "Base",             rpc: "https://rpc.ankr.com/base" },
    { name: "BNB Smart Chain",  rpc: "https://rpc.ankr.com/bsc" },
    { name: "Avalanche C-Chain", rpc: "https://rpc.ankr.com/avalanche" }
];

// Target contract address (assumes deterministic deployment / CREATE2 across chains)
const TARGET_CONTRACT = process.env.CONTRACT_ADDRESS || "0x0000000000000000000000000000000000000000";

// Standard ERC-721 Transfer Event Signature
const TRANSFER_TOPIC = ethers.id("Transfer(address,address,uint256)");

async function attachChainListener(chain) {
    try {
        const provider = new ethers.JsonRpcProvider(chain.rpc);
        
        // Filter for specific contract address if provided, otherwise monitor target topics
        const filter = {
            topics: [TRANSFER_TOPIC]
        };

        if (TARGET_CONTRACT !== "0x0000000000000000000000000000000000000000") {
            filter.address = TARGET_CONTRACT;
        }

        console.log(`[+] Initialized monitor on: ${chain.name}`);

        provider.on(filter, (log) => {
            const from = ethers.dataSlice(log.topics[1], 12);
            const to = ethers.dataSlice(log.topics[2], 12);
            const tokenId = BigInt(log.topics[3]).toString();

            const isMint = from === "0x0000000000000000000000000000000000000000";
            const tag = isMint ? "\x1b[32m[GENESIS MINT]\x1b[0m" : "[TRANSFER]";

            console.log(
                `${tag} Network: ${chain.name} | Token ID: #${tokenId}\n` +
                `    From: ${from}\n` +
                `    To:   ${to}\n` +
                `    Tx:   ${log.transactionHash}\n` +
                `--------------------------------------------------`
            );
        });

    } catch (err) {
        console.error(`[-] Failed to attach listener on ${chain.name}: ${err.message}`);
    }
}

async function main() {
    console.clear();
    console.log("==================================================");
    console.log("    ROBDOE MULTI-CHAIN EVENT LISTENER (TERMUX)   ");
    console.log("==================================================");
    if (TARGET_CONTRACT !== "0x0000000000000000000000000000000000000000") {
        console.log(`Filtering Target Contract: ${TARGET_CONTRACT}`);
    } else {
        console.log("Listening globally for all Transfer events...");
    }
    console.log("==================================================\n");

    for (const chain of CHAINS) {
        await attachChainListener(chain);
    }
}

main();
