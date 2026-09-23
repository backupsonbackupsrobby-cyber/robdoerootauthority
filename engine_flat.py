import time
import math

N = 72
cols = 9
rows = 8
K = 1.618
gamma = 0.1
dt = 0.05
resolution = 0.052  # 0.052 arc resolution scaling

# Map 72 nodes onto a flat 2D surface coordinate grid
coords = []
for r in range(rows):
    for c in range(cols):
        coords.append((c * resolution, r * resolution))

theta = [2.0 * math.pi * i / N for i in range(N)]
omega = [1.0 + 0.1 * math.sin(i) for i in range(N)]
v = [0.0 for i in range(N)]

print(f"[*] Initializing Flat-Surface Kuramoto-Newton Engine ({rows}x{cols} grid, {resolution} arc)...")

try:
    while True:
        v_new = list(v)
        theta_new = list(theta)
        
        for i in range(N):
            # Flat surface spatial coupling based on coordinate distance
            xi, yi = coords[i]
            coupling = 0.0
            for j in range(N):
                if i != j:
                    xj, yj = coords[j]
                    dist = math.sqrt((xi - xj)**2 + (yi - yj)**2)
                    # Distance-weighted interaction on a flat surface
                    weight = 1.0 / (1.0 + dist)
                    coupling += weight * math.sin(theta[j] - theta[i])
            
            accel = omega[i] + (K / N) * coupling - gamma * v[i]
            v_new[i] = v[i] + accel * dt
            theta_new[i] = theta[i] + v_new[i] * dt
            
        v = v_new
        theta = theta_new
        
        r_real = sum(math.cos(t) for t in theta) / N
        r_imag = sum(math.sin(t) for t in theta) / N
        coherence = math.sqrt(r_real**2 + r_imag**2)
        
        print(f"[FLAT-SYNC] Coherence R: {coherence:.4f}", end="\r")
        time.sleep(dt)

except KeyboardInterrupt:
    print("\n[*] Flat-surface engine safely halted. Grid state locked.")
