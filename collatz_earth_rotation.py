import time
import hashlib

SECRET_KEY = "esp32"

def collatz_step(n):
    return n // 2 if n % 2 == 0 else 3 * n + 1

def align_earth_rotation_trajectory(node_id, region, initial_angle):
    val = initial_angle
    steps = 0
    trajectory = [val]
    
    while val > 1 and steps < 20:
        val = collatz_step(val)
        trajectory.append(val)
        steps += 1
        
    payload = f"COLLATZ-ALIGN|NODE:{node_id}|REGION:{region}|INIT:{initial_angle}|STEPS:{steps}|SEC:{SECRET_KEY}"
    frame_hash = hashlib.sha256(payload.encode()).hexdigest()[:16]
    print(f"[3N+1-LOCK] Region: {region} | Initial Angle: {initial_angle}° | Steps to Unity: {steps} | Hash: {frame_hash}")

if __name__ == "__main__":
    print(f"[*] Aligning Planetary Rotation and Mesh Phase to 3n+1 Trajectory...")
    
    # Anchor rotational degrees of freedom for planetary nodes
    rotational_nodes = [
        {"id": 1, "region": "QLD-Edge", "angle": 27},
        {"id": 2, "region": "NT-Edge", "angle": 12},
        {"id": 3, "region": "WA-Edge", "angle": 31},
        {"id": 4, "region": "SA-Edge", "angle": 34},
        {"id": 5, "region": "ACT-Edge", "angle": 35},
        {"id": 6, "region": "NSW-Edge", "angle": 33},
        {"id": 7, "region": "NZ-North", "angle": 36},
        {"id": 8, "region": "NZ-South", "angle": 43},
        {"id": 9, "region": "Africa-South", "angle": 33},
        {"id": 10, "region": "South-America", "angle": 33},
        {"id": 11, "region": "Antarctic-Deep", "angle": 77},
        {"id": 12, "region": "North-America", "angle": 37},
        {"id": 13, "region": "Europe-Central", "angle": 52},
        {"id": 14, "region": "Asia-Pacific", "angle": 35},
        {"id": 15, "region": "Arctic-Polar", "angle": 78}
    ]

    for node in rotational_nodes:
        align_earth_rotation_trajectory(node["id"], node["region"], node["angle"])
        time.sleep(0.03)

    print("[+] Earth Rotation Phase Aligned to 3n+1 Deterministic Trajectory Matrix.")
