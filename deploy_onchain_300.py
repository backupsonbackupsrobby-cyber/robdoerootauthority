import json
import os

def generate_onchain_deployment_package():
    print("[*] Compiling 300 Solo Domains for On-Chain Deployment...")
    
    # Verify metadata exists
    if not os.path.exists("solo_300_metadata"):
        print("[!] Error: 'solo_300_metadata' not found. Run previous generation step first.")
        return

    all_domains = []
    for i in range(300):
        with open(f"solo_300_metadata/{i}.json", "r") as f:
            all_domains.append(json.load(f))

    # Master On-Chain Deployment Manifest
    deployment_package = {
        "contract_name": "SovereignSoloDomains",
        "symbol": "SOLO",
        "total_supply": 300,
        "issuer": "RobDoe Pty Ltd",
        "legal_framework": "Evidence Act 1995 (Cth) s 146",
        "authority_node": "ATOM-TRUTH",
        "tokens": all_domains
    }

    with open("onchain_deployment_payload.json", "w") as f:
        json.dump(deployment_package, f, indent=2)

    print("==================================================")
    print("   ON-CHAIN DEPLOYMENT PACKAGE READY")
    print("==================================================")
    print(f"[+] Total Tokens Packed : 300")
    print(f"[+] Target Standard     : ERC-721 Enumerable")
    print(f"[+] Output File         : ~/robdoerootauthority/onchain_deployment_payload.json")
    print("==================================================")

if __name__ == "__main__":
    generate_onchain_deployment_package()
