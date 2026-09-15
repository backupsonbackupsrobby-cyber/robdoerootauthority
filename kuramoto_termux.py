import math
import cmath

def evaluate_kuramoto_sync(phases, frequencies, coupling_k, dt=0.01, steps=1000):
    N = len(phases)
    for step in range(steps):
        d_phases = []
        for i in range(N):
            coupling_sum = sum(math.sin(phases[j] - phases[i]) for j in range(N))
            d_theta = frequencies[i] + (coupling_k / N) * coupling_sum
            d_phases.append(d_theta)
        phases = [(phases[i] + d_phases[i] * dt) % (2 * math.pi) for i in range(N)]
    
    complex_sum = sum(cmath.exp(1j * theta) for theta in phases) / N
    r = abs(complex_sum)
    psi = cmath.phase(complex_sum)
    return r, psi, phases

phases = [0.1, 0.4, 0.8, 1.2]
freqs = [1.00, 1.01, 0.99, 1.02]
K = 2.5
N = len(phases)

r, psi, locked_phases = evaluate_kuramoto_sync(phases, freqs, K)

print(f"=== KURAMOTO PHASE LOCK REPORT ===")
print(f"Nodes (N)           : {N}")
print(f"Coupling Factor (K) : {K}")
print(f"Order Parameter (r) : {r:.6f}")
print(f"Mean Phase Angle    : {psi:.6f} rad")
print(f"Sync Status         : {'PHASE LOCKED (r -> 1)' if r > 0.95 else 'INCOHERENT'}")
