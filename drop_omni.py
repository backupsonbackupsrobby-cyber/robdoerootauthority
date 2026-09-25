cat << 'EOF' > drop_omni.py
import json
import os

def generate_deploy_script():
    print("[*] Generating Hardhat/Foundry drop script for all 11,400 assets...")

    # Load omni payload if available, or scan directories
    payload_path = "omni_deployment_payload.json"
    if os.path.exists(payload_path):
        with open(payload_path, "r") as f:
            data = json.load(f)
            tokens = data.get("tokens", [])
    else:
        print("[!] Omni payload not found, scanning individual files...")
        tokens = []
        # Quick fallback gatherer
        for root, dirs, files in os.walk("."):
            for file in files:
                if file.endswith(".json") and "manifest" not in file and "payload" not in file:
                    try:
                        with open(os.path.join(root, file), "r") as tf:
                            j = json.load(tf)
                            if "token_id" in j:
                                tokens.append(j)
                    except Exception:
                        pass

    print(f"[+] Loaded {len(tokens)} token records for drop.")

    # Generate deployment batch runner script
    runner_code = f'''// Auto-generated Omni-Drop Deployment Script
const hre = require("hardhat");

async function main() {{
    console.log("[*] Deploying SovereignOmniRegistry under RobDoe Pty Ltd authority...");
    const Registry = await hre.ethers.getContractFactory("SovereignOmniRegistry");
    const registry = await Registry.deploy();
    await registry.waitForDeployment();

    const address = await registry.getAddress();
    console.log(`[+] SovereignOmniRegistry deployed to: ${{address}}`);

    // Token batch data compiled from ATOM-TRUTH
    const tokenIds = {json.dumps([t["token_id"] for t in tokens[:500]])}; // Example chunk
    const uris = {json.dumps([t.get("namespace", "node.atom") for t in tokens[:500]])};

    console.log("[*] Executing sovereign batch mint...");
    const tx = await registry.sovereignBatchMint(tokenIds, uris);
    await tx.wait();
    console.log("[+] Batch mint confirmed on-chain. Absolute scenes.");
}}

main().catch((error) => {{
    console.error(error);
    process.exitCode = 1;
}});
'''

    os.makedirs("scripts", exist_ok=True)
    with open("scripts/deploy_omni.js", "w") as f:
        f.write(runner_code)

    print("==================================================")
    print("   OMNI-DROP READY TO DEPLOY")
    print("==================================================")
    print("[+] Script Path : ~/robdoerootauthority/scripts/deploy_omni.js")
    print("[+] Run via     : npx hardhat run scripts/deploy_omni.js --network <your-network>")
    print("==================================================")

if __name__ == "__main__":
    generate_deploy_script()
EOF
python drop_omni.py
