import hashlib
import json
import os

def create_xyo_witness(chain_file="sovereign_miner.py"):
    print("[*] Generating XYO Bound Witness cryptographic proof...")
    payload = open(chain_file, "r").read() if os.path.exists(chain_file) else "ATOM-TRUTH-GENESIS-ANCHOR"
    device_anchor = "Moto-G06-Termux-ATOM-TRUTH"
    witness_data = f"{payload}:{device_anchor}:{os.path.exists('.git')}"
    witness_hash = hashlib.sha256(witness_data.encode()).hexdigest()

    proof = {
        "protocol": "XYO-Bound-Witness-v1",
        "device": device_anchor,
        "payload_hash": hashlib.sha256(payload.encode()).hexdigest(),
        "witness_hash": witness_hash,
        "timestamp": os.path.getmtime(chain_file) if os.path.exists(chain_file) else 0
    }

    with open("xyo_proof.json", "w") as pf:
        json.dump(proof, pf, indent=4)
    print(f"[+] XYO Witness Bound! Proof Hash: {witness_hash[:16]}...")

if __name__ == "__main__":
    create_xyo_witness()
