cat << 'EOF' > scripts/mint_sovereign.js
import hre from "hardhat";

async function main() {
  const contractAddress = process.env.CONTRACT_ADDRESS || "0x5FbDB2315678afecb367f032d93F642f64180aa3";
  
  const SovereignAuthorityNFT = await hre.ethers.getContractFactory("SovereignAuthorityNFT");
  const sovereign = SovereignAuthorityNFT.attach(contractAddress);

  const [deployer] = await hre.ethers.getSigners();
  const rootHashUri = "urn:sha256:204ef68b19bd41c3dfac098f6f6cfb22e448fa090844da6075d448a75c094088";

  console.log(`Minting Sovereign Root Token to: ${deployer.address}`);
  const tx = await sovereign.mintSovereignToken(deployer.address, rootHashUri);
  await tx.wait();

  console.log(`[LOCKED] Sovereign Token Minted with URI: ${rootHashUri}`);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
EOF

