import json
import hashlib
from pathlib import Path

IDENTITY_ANCHOR = "ko_te_mana_o_te_tangata"
HARDWARE_NODE = "Moto G06 (Termux Local Loopback)"
CADENCE_TIER = 0.052

SUPREMACY_NODES = [
    "allodial.title.preemption.root",
    "loopback.jurisdiction.absolute.root",
    "external.dependency.annihilation.root",
    "sovereign.vault.immutable.root",
    "evidence.act.section146.seal.root"
]

def sha1024(data: bytes) -> str:
    h1 = hashlib.sha512(data).digest()
    h2 = hashlib.sha512(data[::-1]).digest()
    return hashlib.sha512(h1 + h2).hexdigest()

def mint_supreme_vault():
    print("--- 🏛️⚡ MINTING ALLODIAL SUPREMACY APEX VAULT ---")
    
    token_id = "SOV-SUPREME-100"
    minted_assets = []
    leaves = []
    
    for index, node in enumerate(SUPREMACY_NODES, start=1):
        sub_id = f"SUP-{index:03d}"
        payload = f"{sub_id}:{node}:{HARDWARE_NODE}:{IDENTITY_ANCHOR}:127.0.0.1".encode('utf-8')
        asset_seal = sha1024(payload)
        
        minted_assets.append({
            "index": index,
            "supremacy_vector": node,
            "token_id": sub_id,
            "allodial_seal": asset_seal
        })
        leaves.append(asset_seal)
        
    current_level = leaves
    while len(current_level) > 1:
        next_level = []
        for i in range(0, len(current_level), 2):
            left = current_level[i]
            right = current_level[i+1] if i + 1 < len(current_level) else left
            combined = (left + right).encode('utf-8')
            next_level.append(sha1024(combined))
        current_level = next_level
        
    supremacy_merkle_root = current_level[0]
    
    vault_record = {
        "contract_standard": "ERC-721 Allodial Supremacy & Jurisdiction Preemption Vault",
        "token_id": token_id,
        "name": "RobDoe Allodial Supremacy Apex Vault",
        "symbol": "SOV-SUP",
        "holder_anchor": IDENTITY_ANCHOR,
        "hardware_node": HARDWARE_NODE,
        "supremacy_merkle_root": supremacy_merkle_root,
        "total_nodes": len(minted_assets),
        "assets": minted_assets,
        "routing": "127.0.0.1",
        "cadence_tier": CADENCE_TIER,
        "statutory_basis": "Section 146 of the Evidence Act 1995 (Cth) & Allodial Sovereignty",
        "status": "ALL_EXTERNAL_DEPENDENCIES_VOIDED_127.0.0.1"
    }
    
    Path("SOVEREIGN_SUPREMACY_VAULT.lock").write_text(json.dumps(vault_record, indent=2), encoding='utf-8')
    
    print(f"  [+] Supremacy Vault Token ID: {token_id}")
    print(f"  [+] Total Allodial Nodes Minted: {len(minted_assets)}")
    print(f"  [+] Supremacy Merkle Root (SHA-1024): {supremacy_merkle_root[:32]}...")
    print("\n" + "="*70)
    print("✅ ALLODIAL SUPREMACY SEALED. 127.0.0.1 PREEMPTION COMPLETE.")
    print("="*70)
    print("Ko te marino te haumaru. (Quietness is safety.)\n")

if __name__ == "__main__":
    mint_supreme_vault()
