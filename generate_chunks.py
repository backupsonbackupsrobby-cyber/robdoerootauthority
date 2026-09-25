import json
import os

def generate_chunked_scripts():
    print("[*] Reading omni deployment payload...")
    payload_path = "omni_deployment_payload.json"
    if not os.path.exists(payload_path):
        print("[!] Omni payload not found!")
        return

    with open(payload_path, "r") as f:
        data = json.load(f)
        tokens = data.get("tokens", [])

    print(f"[+] Total loaded tokens: {len(tokens)}")

    chunk_size = 5000
    chunk_1 = tokens[:chunk_size]
    chunk_2 = tokens[chunk_size:]

    c1_ids = [t["token_id"] for t in chunk_1]
    c1_uris = [t.get("namespace", "node.atom") for t in chunk_1]

    # Using standard string concatenation inside the f-string to avoid curly brace collision
    script_1 = "// Chunk 1: Sovereign 5,000 Asset Bundle\n" + \
"const hre = require(\"hardhat\");\n\n" + \
"async function main() {\n" + \
"    console.log(\"[*] Deploying SovereignOmniRegistry (Chunk 1: 5,000 Assets)...\");\n" + \
"    const Registry = await hre.ethers.getContractFactory(\"SovereignOmniRegistry\");\n" + \
"    const registry = await Registry.deploy();\n" + \
"    await registry.waitForDeployment();\n" + \
"    const address = await registry.getAddress();\n" + \
"    console.log(`[+] Contract deployed to: ${address}`);\n\n" + \
"    const tokenIds = " + json.dumps(c1_ids) + ";\n" + \
"    const uris = " + json.dumps(c1_uris) + ";\n\n" + \
"    const batchSize = 500;\n" + \
"    for (let i = 0; i < tokenIds.length; i += batchSize) {\n" + \
"        const bIds = tokenIds.slice(i, i + batchSize);\n" + \
"        const bUris = uris.slice(i, i + batchSize);\n" + \
"        console.log(`[*] Minting batch ${Math.floor(i / batchSize) + 1} (${bIds.length} assets)...`);\n" + \
"        const tx = await registry.sovereignBatchMint(bIds, bUris);\n" + \
"        await tx.wait();\n" + \
"    }\n" + \
"    console.log(\"[+] Chunk 1 (5,000 Bundle) successfully minted on-chain!\");\n" + \
"}\n\n" + \
"main().catch((error) => { console.error(error); process.exitCode = 1; });\n"

    os.makedirs("scripts/chunks", exist_ok=True)
    with open("scripts/chunks/deploy_chunk_1.js", "w") as f:
        f.write(script_1)

    if chunk_2:
        c2_ids = [t["token_id"] for t in chunk_2]
        c2_uris = [t.get("namespace", "node.atom") for t in chunk_2]

        script_2 = "// Chunk 2: Remaining Solo Assets (" + str(len(chunk_2)) + " tokens)\n" + \
"const hre = require(\"hardhat\");\n\n" + \
"async function main() {\n" + \
"    const registryAddress = \"YOUR_DEPLOYED_CONTRACT_ADDRESS\";\n" + \
"    console.log(\"[*] Connecting to SovereignOmniRegistry for solo remainder...\");\n" + \
"    const Registry = await hre.ethers.getContractFactory(\"SovereignOmniRegistry\");\n" + \
"    const registry = Registry.attach(registryAddress);\n\n" + \
"    const tokenIds = " + json.dumps(c2_ids) + ";\n" + \
"    const uris = " + json.dumps(c2_uris) + ";\n\n" + \
"    const batchSize = 500;\n" + \
"    for (let i = 0; i < tokenIds.length; i += batchSize) {\n" + \
"        const bIds = tokenIds.slice(i, i + batchSize);\n" + \
"        const bUris = uris.slice(i, i + batchSize);\n" + \
"        console.log(`[*] Minting solo batch ${Math.floor(i / batchSize) + 1} (${bIds.length} assets)...`);\n" + \
"        const tx = await registry.sovereignBatchMint(bIds, bUris);\n" + \
"        await tx.wait();\n" + \
"    }\n" + \
"    console.log(\"[+] All remaining solo assets minted successfully. Empire complete.\");\n" + \
"}\n\n" + \
"main().catch((error) => { console.error(error); process.exitCode = 1; });\n"

        with open("scripts/chunks/deploy_chunk_2_solo.js", "w") as f:
            f.write(script_2)

    print("==================================================")
    print("   CHUNKS GENERATED SUCCESSFULLY")
    print("==================================================")
    print("[+] Chunk 1 (5,000 Bundle): scripts/chunks/deploy_chunk_1.js")
    print(f"[+] Chunk 2 (Solo Rest)  : scripts/chunks/deploy_chunk_2_solo.js ({len(chunk_2)} assets)")
    print("==================================================")

if __name__ == "__main__":
    generate_chunked_scripts()
