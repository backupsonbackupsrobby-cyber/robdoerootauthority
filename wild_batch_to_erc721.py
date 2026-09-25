import json
import hashlib
import subprocess
import os

def get_git_commit_hash():
    try:
        result = subprocess.run(['git', 'rev-parse', 'HEAD'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode == 0:
            return result.stdout.strip()
    except Exception:
        pass
    return "e14f9a8d00000000000000000000000000000000000000000000000000000000"

def mint_wild_batch():
    print("[*] Minting wild-card sovereign infrastructure, AI, financial, and hardware assets...")
    git_head = get_git_commit_hash()
    
    targets = [
        {"name": "Emergency Dispatch 000", "symbol": "000", "id": 1100, "ns": "000.atom", "class": "Emergency Infrastructure"},
        {"name": "Emergency Dispatch 111", "symbol": "111", "id": 1101, "ns": "111.atom", "class": "Emergency Infrastructure"},
        {"name": "Internet Root DNS", "symbol": "ROOT", "id": 1102, "ns": "root.atom", "class": "Global Core Network"},
        {"name": "Pentagon Defense Node", "symbol": "PENTAGON", "id": 1103, "ns": "pentagon.atom", "class": "Defense & Aerospace"},
        {"name": "CERN Research Facility", "symbol": "CERN", "id": 1104, "ns": "cern.atom", "class": "Particle Physics Lab"},
        {"name": "OpenAI Sovereign Node", "symbol": "OAI", "id": 1105, "ns": "openai.atom", "class": "Foundational AI Model"},
        {"name": "Anthropic Sovereign Node", "symbol": "ANTH", "id": 1106, "ns": "anthropic.atom", "class": "Foundational AI Model"},
        {"name": "DeepSeek Sovereign Node", "symbol": "DS", "id": 1107, "ns": "deepseek.atom", "class": "Foundational AI Model"},
        {"name": "Skynet Neural Matrix", "symbol": "SKY", "id": 1108, "ns": "skynet.atom", "class": "Autonomous Multi-Agent"},
        {"name": "Federal Reserve Core", "symbol": "FED", "id": 1109, "ns": "fed.atom", "class": "Central Bank Settlement"},
        {"name": "SWIFT Settlement Layer", "symbol": "SWIFT", "id": 1110, "ns": "swift.atom", "class": "Global Wire Routing"},
        {"name": "ESP32 Hardware Core", "symbol": "ESP32", "id": 2026, "ns": "esp32.atom", "class": "Embedded Edge IoT"}
    ]

    os.makedirs("wild_nfts", exist_ok=True)
    master_manifest = []

    for item in targets:
        raw_data = f"{item['id']}:{item['name']}:{git_head}:RobDoePtyLtd".encode('utf-8')
        root_hash = hashlib.sha256(raw_data).hexdigest()

        metadata = {
            "name": f"{item['name']} Sovereign Asset",
            "symbol": item["symbol"],
            "description": f"Sovereign cryptographic representation of {item['name']} under RobDoe Pty Ltd authority.",
            "token_id": item["id"],
            "namespace": item["ns"],
            "issuer": "RobDoe Pty Ltd",
            "legal_framework": "Evidence Act 1995 (Cth) s 146",
            "git_commit_hash": git_head,
            "individual_root_hash": f"0x{root_hash}",
            "attributes": [
                {"trait_type": "Asset Class", "value": item["class"]},
                {"trait_type": "Authority", "value": "ATOM-TRUTH"},
                {"trait_type": "Jurisdiction", "value": "Australia"}
            ]
        }

        filename = f"wild_nfts/{item['symbol'].lower()}_token.json"
        with open(filename, "w") as f:
            json.dump(metadata, f, indent=2)
        
        master_manifest.append(metadata)
        print(f"[+] Locked: {item['ns']} (ID: {item['id']}) -> {filename}")

    with open("wild_nfts/master_wild_manifest.json", "w") as f:
        json.dump(master_manifest, f, indent=2)

    print("==================================================")
    print("   ALL WILD-CARD ASSETS SUCCESSFULLY MINTED")
    print("==================================================")
    print(f"[+] Total Assets Created : {len(targets)}")
    print(f"[+] Master Manifest      : ~/robdoerootauthority/wild_nfts/master_wild_manifest.json")
    print("==================================================")

if __name__ == "__main__":
    mint_wild_batch()
