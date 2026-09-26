import os
import sys
import time
import math
import cmath
import hashlib

# ------------------------------------------------------------------
# 1. KURAMOTO PHASE SYNCHRONIZATION ENGINE
# ------------------------------------------------------------------
class PhaseRing:
    def __init__(self, num_nodes=4, coupling_k=1.5):
        self.N = num_nodes
        self.K = coupling_k
        self.theta = [i * (2 * math.pi / num_nodes) for i in range(num_nodes)]
        self.omega = [1.0 + (i * 0.05) for i in range(num_nodes)]

    def step(self, dt=0.1):
        new_theta = []
        for i in range(self.N):
            coupling_sum = sum(
                math.sin(self.theta[j] - self.theta[i]) 
                for j in range(self.N)
            )
            d_theta = self.omega[i] + (self.K / self.N) * coupling_sum
            new_theta.append((self.theta[i] + d_theta * dt) % (2 * math.pi))
        self.theta = new_theta

    def order_parameter(self) -> float:
        """Returns R(t): Phase cohesion score (0.0 = chaos, 1.0 = absolute lock)"""
        z = sum(cmath.exp(1j * th) for th in self.theta) / self.N
        return abs(z)

# ------------------------------------------------------------------
# 2. STATE MERKLE ROOT CALCULATOR
# ------------------------------------------------------------------
def compute_merkle_root(leaves: list[bytes]) -> str:
    if not leaves:
        return "0" * 64
    layer = [hashlib.sha256(leaf).digest() for leaf in leaves]
    while len(layer) > 1:
        if len(layer) % 2 != 0:
            layer.append(layer[-1])
        layer = [
            hashlib.sha256(layer[i] + layer[i+1]).digest() 
            for i in range(0, len(layer), 2)
        ]
    return layer[0].hex()

# ------------------------------------------------------------------
# 3. TERMUX HARDWARE LOOP & TERMINAL DASHBOARD
# ------------------------------------------------------------------
def run_runtime():
    ring = PhaseRing(num_nodes=4, coupling_k=2.1)
    nodes = ["ESP32-M1", "ATOM-MATRIX-M2", "NRF24-LINK-M3", "TERMUX-HOST-M4"]

    print("\033[2J\033[H") # Clear terminal
    print("\033[1;36m=== TERMUX SOVEREIGN MERKLE RUNTIME INITIALIZED ===\033[0m\n")

    try:
        step_count = 0
        while True:
            ring.step(dt=0.05)
            cohesion = ring.order_parameter()
            
            # Construct leaf states anchored to node phases
            leaves = [
                f"{node}:{ring.theta[idx]:.6f}:{step_count}".encode('utf-8')
                for idx, node in enumerate(nodes)
            ]
            merkle_root = compute_merkle_root(leaves)

            # Render ASCII Telemetry
            sys.stdout.write("\033[H")
            print(f"\033[1;33m[TERMUX NODE]\033[0m Processing Frame: \033[1;32m#{step_count:06d}\033[0m")
            print(f"\033[1;33m[PHASE LOCK ]\033[0m Order Parameter R(t): \033[1;35m{cohesion:.6f}\033[0m")
            print(f"\033[1;33m[MERKLE ROOT]\033[0m \033[1;34m0x{merkle_root}\033[0m\n")
            
            print("--- ACTIVE TELEMETRY RING ---")
            for idx, node in enumerate(nodes):
                bar = "#" * int(ring.theta[idx] * 4)
                print(f"{node:<16} | Phase: {ring.theta[idx]:.4f} rad | [{bar:<26}]")

            sys.stdout.flush()
            time.sleep(0.1)
            step_count += 1

    except KeyboardInterrupt:
        print("\n\n\033[1;31m[!] Pipeline suspended cleanly.\033[0m")

if __name__ == "__main__":
    run_runtime()
