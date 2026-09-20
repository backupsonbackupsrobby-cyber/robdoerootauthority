cat << 'EOF' > scripts/deploy.js
import hre from "hardhat";

async function main() {
  const sovereignAuthority = await hre.ethers.deployContract("SovereignAuthorityNFT");
  await sovereignAuthority.waitForDeployment();
  console.log(`SovereignAuthorityNFT deployed to: ${await sovereignAuthority.getAddress()}`);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
EOF

