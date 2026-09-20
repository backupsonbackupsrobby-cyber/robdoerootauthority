import { ethers } from "ethers";
import fs from "fs";

async function main() {
  // Connect to local or fallback provider
  const provider = new ethers.JsonRpcProvider("http://127.0.0.1:8545");
  console.log("[CONNECT] Vector established across local RPC.");
}

main().catch(console.error);
