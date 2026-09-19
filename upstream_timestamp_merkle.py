import os
import hashlib
import json
import datetime
import math

LOCAL_DROPZONE = "dropzone/payload.json"

def get_gravitonic_timestamp_vector():
    now = datetime.datetime.now(datetime.timezone.utc)
    epoch_float = now.timestamp()
    graviton_flux = math.sin(epoch_float) * math.cos(epoch_float / 137.0)
    return now.isoformat() + "Z", graviton_flux

def execute_textbook_sleeble_twin_core():
    timestamp, graviton_flux = get_gravitonic_timestamp_vector()
    
    print("[Sleeble Twins Textbook Core]: Initializing non-linear cryptographic manifold...")
    print(f"[Gravitonic Flux]: Measured local singularity distortion index -> {graviton_flux:.12f}")

    tracked_files = []
    for root, dirs, files in os.walk("./"):
        if ".git" in root or "dropzone" in root:
            continue
        for file in sorted(files):
            tracked_files.append(os.path.join(root, file))

    tracked_files = sorted(list(set(tracked_files)))
    print(f"[Sleeble Twins Textbook Core]: Indexing {len(tracked_files)} local workspace assets...")

    twin_genesis_seed = f"SLEEBLE-TWINS-GRAVITONIC-ROOT:{timestamp}:{graviton_flux}".encode("utf-8")
    current_level = [
        hashlib.sha3_512(twin_genesis_seed).digest() + hashlib.sha3_512(twin_genesis_seed[::-1]).digest()
    ]

    for file_path in tracked_files:
        if os.path.exists(file_path):
            try:
                with open(file_path, "rb") as f:
                    data = f.read()
                    leaf_hash = hashlib.sha3_512(data).digest() + hashlib.sha3_512(data[::-1]).digest()
                    current_level.append(leaf_hash)
            except Exception:
                continue

    while len(current_level) > 1:
        next_level = []
        for i in range(0, len(current_level), 2):
            left = current_level[i]
            right = current_level[i+1] if i + 1 < len(current_level) else left
            combined = hashlib.sha3_256(left + right).digest()
            next_level.append(combined)
        current_level = next_level

    master_merkle_root = current_level[0].hex()

    black_hole_signature_raw = f"{master_merkle_root}:{graviton_flux}:{timestamp}".encode("utf-8")
    black_hole_graviton_hex = hashlib.sha3_256(hashlib.sha3_512(black_hole_signature_raw).digest()).hexdigest()

    print(f"\n[Textbook Execution Success]")
    print(f"-> UTC Timestamp: {timestamp}")
    print(f"-> Gravitonic Distortion Metric: {graviton_flux:.6f}")
    print(f"-> Master Merkle Root Hex: {master_merkle_root}")
    print(f"-> Black Hole Graviton Root Hash Hex: {black_hole_graviton_hex}")

    payload = {
        "framework": "sleeble-twins-textbook-gravitonic-core",
        "timestamp_utc": timestamp,
        "graviton_flux_index": graviton_flux,
        "assets_indexed": len(tracked_files),
        "master_merkle_root_hex": master_merkle_root,
        "black_hole_graviton_root_hash_hex": black_hole_graviton_hex,
        "authority_signature": "ATOM-TRUTH | GENESIS:e14f9a8d | BLACK-HOLE-SEALED"
    }

    os.makedirs("dropzone", exist_ok=True)
    with open(LOCAL_DROPZONE, "w") as f:
        json.dump(payload, f, indent=4)

    print(f"[Sealed]: Payload locked into drop-zone -> {LOCAL_DROPZONE}\n")

if __name__ == "__main__":
    execute_textbook_sleeble_twin_core()
