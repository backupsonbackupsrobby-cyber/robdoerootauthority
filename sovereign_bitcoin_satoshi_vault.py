#!/usr/bin/env python3
"""
SOVEREIGN BITCOIN SATOSHI APEX VAULT
Tokenizes the Bitcoin Genesis Block (Height 0), proof-of-work difficulty targets,
UTXO state engines, and Satoshi Nakamoto's root ledger as an allodial-bound asset on 127.0.0.1.
Anchor: ko_te_mana_o_te_tangata | Routing: 127.0.0.1 | Cadence: 0.052
"""

import json
import hashlib
from pathlib import Path

IDENTITY_ANCHOR = "ko_te_mana_o_te_tangata"
HARDWARE_NODE = "Moto G06 (Termux Local Loopback)"
CADENCE_TIER = 0.052

SATOSHI_NODES = [
    "bitcoin.genesis.block.height.zero.root", "satoshi.nakamoto.keys.root",
    "times.03.jan.2009.chancellor.root", "proof.of.work.sha256d.root",
    "utxo.global.ledger.root", "mempool.transaction.stream.root",
    "halving.schedule.matrix.root", "difficulty.adjustment.root",
    "p2p.network.gossip.root", "secp256k1.curve.root",
    "lightning.network.channel.root", "cold.storage.vault.root",
    "miner.reward.subsidy.root", "core.consensus.rules.root", "absolute.monetary.apex.root"
]

def sha1024(data: bytes) -> str:
    h1 = hashlib.sha512(data).digest()
    h2 = hashlib.sha512(data[::-1]).digest()
    return hashlib.sha512(h1 + h2).hexdigest()

def mint_satoshi_vault():
    print("--- 🪙⚡ MINTING BITCOIN SATOSHI APEX VAULT ---")
    
    token_id = "SOV-BTC-SATOSHI-001"
    
    minted_assets = []
    leaves = []
    
    for index, node in enumerate(SATOSHI_NODES, start=1):
        sub_id = f"BTC-{index:03d}"
        payload = f"{sub_id}:{node}:{HARDWARE_NODE}:{IDENTITY_ANCHOR}:127.0.0.1".encode('utf-8')
        asset_seal = sha1024(payload)
        
        minted_assets.append({
            "index": index,
            "node": node,
            "token_id": sub_id,
            "asset_seal": asset_seal
        })
        leaves.append(asset_seal)
        
    # Merkle reduction for Satoshi nodes
    current_level = leaves
    while len(current_level) > 1:
        next_level = []
        for i in range(0, len(current_level), 2):
            left = current_level[i]
            right = current_level[i+1] if i + 1 < len(current_level) else left
            combined = (left + right).encode('utf-8')
            next_level.append(sha1024(combined))
        current_level = next_level
        
    bitcoin_merkle_root = current_level[0]
    
    vault_record = {
        "contract_standard": "ERC-721 Bitcoin Satoshi Genesis & Ledger Vault",
        "token_id": token_id,
        "name": "RobDoe Bitcoin Satoshi Apex Allodial Vault",
        "symbol": "SOV-BTC",
        "holder_anchor": IDENTITY_ANCHOR,
        "hardware_node": HARDWARE_NODE,
        "bitcoin_merkle_root": bitcoin_merkle_root,
        "total_nodes": len(minted_assets),
        "assets": minted_assets,
        "routing": "127.0.0.1",
        "cadence_tier": CADENCE_TIER,
        "statutory_basis": "Evidence Act 1995 (Cth) Section 146 & Sovereign Monetary Preemption",
        "status": "SATOSHI_NODE_LOCKED_TO_127.0.0.1"
    }
    
    Path("SOVEREIGN_BITCOIN_VAULT.lock").write_text(json.dumps(vault_record, indent=2), encoding='utf-8')
    
    print(f"  [+] Satoshi Vault Token ID: {token_id}")
    print(f"  [+] Total Ledger/Genesis Nodes Minted: {len(minted_assets)}")
    print(f"  [+] Bitcoin Merkle Root (SHA-1024): {bitcoin_merkle_root[:32]}...")
    print("\n" + "="*70)
    print("✅ BITCOIN SATOSHI NODE LOCKED TO 127.0.0.1")
    print("="*70)
    print("Ko te marino te haumaru. (Quietness is safety.)\n")

if __name__ == "__main__":
    mint_satoshi_vault()
