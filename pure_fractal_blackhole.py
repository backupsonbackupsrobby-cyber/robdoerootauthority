import os
import hashlib
import json

TARGET_DIR = "./zsh-copilot"
LOCAL_DROPZONE = "dropzone/payload.json"
MAX_ITERATIONS = 1296000

def compute_fractal_basin(c_real, c_im):
    z = complex(0, 0)
    c = complex(c_real, c_im)
    for i in range(MAX_ITERATIONS):
        if abs(z) > 2.0:
            return i
        z = z*z + c
    return MAX_ITERATIONS

def build_blackhole_grafting_tree(directory):
    current_level = []
    
    # Generate spatial gravitational seed from fractal basin center
    basin_val = compute_fractal_basin(-0.743643887037158704752191506114774, 0.131825904205311970493132056385139)
    seed_bytes = f"blackhole-grafting-basin-{basin_val}".encode('utf-8')
    current_level.append(hashlib.sha512(seed_bytes).digest() + hashlib.sha512(seed_bytes[::-1]).digest())

    for root, dirs, files in os.walk(directory):
        for file in sorted(files):
            file_path = os.path.join(root, file)
            try:
                with open(file_path, "rb") as f:
                    file_data = f.read()
                    h = hashlib.sha512(file_data).digest() + hashlib.sha512(file_data[::-1]).digest()
                    current_level.append(h)
            except Exception:
                continue

    while len(current_level) > 1:
        next_level = []
        for i in range(0, len(current_level), 2):
            left = current_level[i]
            right = current_level[i+1] if i + 1 < len(current_level) else left
            combined = hashlib.sha256(left + right).digest()
            next_level.append(combined)
        current_level = next_level

    return current_level[0].hex(), basin_val

def execute():
    print(f"[Math Engine]: Initializing 2D Black Hole Grafting Tree with {MAX_ITERATIONS} iteration basins...")
    root_hex, basin = build_blackhole_grafting_tree(TARGET_DIR)
    print(f"[Success] Fractal Basin Depth: {basin}")
    print(f"[Success] 2D Black Hole Grafting Root: {root_hex}")

    payload = {
        "framework": "fractal-blackhole-grafting",
        "iterations": MAX_ITERATIONS,
        "basin_signature": basin,
        "merkle_root": root_hex
    }

    with open(LOCAL_DROPZONE, "w") as f:
        json.dump(payload, f, indent=4)
    print(f"[Success] Black hole payload locked into drop-zone: {LOCAL_DROPZONE}")

if __name__ == "__main__":
    execute()
