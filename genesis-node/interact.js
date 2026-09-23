const { ethers } = require("ethers");
require("dotenv").config();

const RPC_URL = process.env.RPC_URL || "https://rpc.ankr.com/eth"; // Replace with your chain RPC
const CONTRACT_ADDRESS = process.env.CONTRACT_ADDRESS || "0xYOUR_CONTRACT_ADDRESS";

// Minimal ERC-721 ABI
const abi = [
  "function name() view returns (string)",
  "function symbol() view returns (string)",
  "function totalSupply() view returns (uint256)",
  "function ownerOf(uint256 tokenId) view returns (address)",
  "event Transfer(address indexed from, address indexed to, uint256 indexed tokenId)"
];

async function main() {
  const provider = new ethers.JsonRpcProvider(RPC_URL);
  const contract = new ethers.Contract(CONTRACT_ADDRESS, abi, provider);

  console.log(`Connecting to contract at ${CONTRACT_ADDRESS}...`);

  try {
    const name = await contract.name();
    const symbol = await contract.symbol();
    console.log(`Token: ${name} (${symbol})`);

    // Listen for real-time mints/transfers directly in Termux
    console.log("Listening for Transfer events...");
    contract.on("Transfer", (from, to, tokenId) => {
      console.log(`[TRANSFER] Token #${tokenId.toString()} | From: ${from} -> To: ${to}`);
    });
  } catch (err) {
    console.error("Error reading contract:", err.message);
  }
}

main();
