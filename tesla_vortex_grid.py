import math
import hashlib

IDENTITY_ANCHOR = "ko_te_mana_o_te_tangata"
CADENCE = "Sha1296000arc"
VORTEX_ROOT = "0f650b1a696876cd7906dfb6c53c7b9ec2816e30a2de20bb385e651f76210ba1"

def compute_tesla_cv():
    # Derive complex constant C_v from the 3-6-9 vortex hash
    h_bytes = bytes.fromhex(VORTEX_ROOT)
    real_part = int.from_bytes(h_bytes[:4], 'big') / 0xFFFFFFFF * 2 - 1
    imag_part = int.from_bytes(h_bytes[4:8], 'big') / 0xFFFFFFFF * 2 - 1
    return complex(real_part, imag_part)

def render_232_grid():
    print("--- 2-3-2 TESLA 369 VORTEX MATRIX ---")
    print(f"Anchor: {IDENTITY_ANCHOR} | Cadence: {CADENCE}")
    
    cv = compute_tesla_cv()
    print(f"Computed Vortex Constant (Cv): {cv}")
    
    # 2-3-2 Layout Layers
    layers = {
        "TOP_ROW (2 Circles)": [1, 2],
        "MIDDLE_ROW (3 Tesla Nodes)": [3, 6, 9],
        "BOTTOM_ROW (2 Anchors)": [7, 8]
    }
    
    grid_state = {}
    
    for layer_name, nodes in layers.items():
        layer_results = []
        for node in nodes:
            # Apply z = z^2 + Cv mapping iteration
            z = complex(node / 3.0, node / 9.0)
            for _ in range(3):  # 3-phase Tesla iteration
                z = (z ** 2) + cv
            magnitude = abs(z)
            phase = math.atan2(z.imag, z.real)
            layer_results.append((node, round(magnitude, 4), round(phase, 4)))
        grid_state[layer_name] = layer_results

    print("\n--- MATRIX TOPOLOGY MAPPING ---")
    for row, data in grid_state.items():
        print(f"\n[{row}]")
        for node, mag, phs in data:
            # Tesla 369 visual indicator scaling
            indicator = "⚡" if node in [3, 6, 9] else "•"
            print(f"  Node {node} {indicator} -> Magnitude: {mag:6.4f} | Phase: {phs:6.4f}")

    # Generate spatial coordinate hash proof
    grid_payload = str(grid_state).encode('utf-8')
    spatial_hash = hashlib.sha256(grid_payload).hexdigest()
    print(f"\nSpatial Vortex Grid Hash: {spatial_hash}")

if __name__ == "__main__":
    render_232_grid()
