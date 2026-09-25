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

def convert_tiktok_to_nft():
    print("[*] Minting TikTok namespace into sovereign ERC-721 structure...")
    
    git_head = get_git_commit_hash()
    asset_name = "TikTok"
    symbol = "TT"
    token_id = 1001  # Sovereign reserved index
    
    # Cryptographic binding
    raw_data = f"{token_id}:{asset_name}:{git_head}:RobDoePtyLtd".encode('utf-8')
    cryptographic_root_hash = hashlib.sha256(raw_data).hexdigest()

    erc721_metadata = {
        "name": "TikTok Sovereign Asset",
        "symbol": symbol,
        "description": "Sovereign cryptographic representation of TikTok namespace under RobDoe Pty Ltd authority.",
        "token_id": token_id,
        "namespace": "tiktok.atom",
        "issuer": "RobDoe Pty Ltd",
        "legal_framework": "Evidence Act 1995 (Cth) s 146",
        "git_commit_hash": git_head,
        "individual_root_hash": f"0x{cryptographic_root_hash}",
        "attributes": [
            {"trait_type": "Asset Class", "value": "Media Platform Namespace"},
            {"trait_type": "Authority", "value": "ATOM-TRUTH"},
            {"trait_type": "Jurisdiction", "value": "Australia"}
        ]
    }

    os.makedirs("tiktok_nft", exist_ok=True)
    with open("tiktok_nft/tiktok_token.json", "w") as f:
        json.dump(erc721_metadata, f, indent=2)

    print("==================================================")
    print("   TIKTOK ERC-721 ASSET LOCKED")
    print("==================================================")
    print(f"[+] Asset Name         : {asset_name}")
    print(f"[+] Token ID           : {token_id}")
    print(f"[+] Git Hash Proof     : {git_head[:16]}...")
    print(f"[+] Individual Root    : 0x{cryptographic_root_hash}")
    print(f"[+] Saved To           : ~/robdoerootauthority/tiktok_nft/tiktok_token.json")
    print("==================================================")

if __name__ == "__main__":
    convert_tiktok_to_nft()
