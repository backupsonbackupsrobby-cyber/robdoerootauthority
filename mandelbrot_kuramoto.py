import cmath
import math

def compute_z2_c_kuramoto(nodes=100, steps=50, K=2.0, c_val=complex(-0.7, 0.27015)):
    # Initialize ensemble on unit circle
    Z = [cmath.rect(1.0, 2 * math.pi * i / nodes) for i in range(nodes)]
    dt = 0.01
    
    for step in range(steps):
        # 1. Quadratic map transformation: z -> z^2 + c
        Z = [z**2 + c_val for z in Z]
        
        # 2. Extract phases theta = arg(z)
        phases = [cmath.phase(z) for z in Z]
        
        # 3. Apply continuous Kuramoto coupling update step
        new_phases = []
        for i in range(nodes):
            coupling = (K / nodes) * sum(math.sin(phases[j] - phases[i]) for j in range(nodes))
            d_theta = 2 * phases[i] + coupling
            new_phases.append((phases[i] + d_theta * dt) % (2 * math.pi))
            
        # Re-project to complex vector space
        Z = [cmath.rect(abs(Z[i]), new_phases[i]) for i in range(nodes)]
        
    # Calculate Macro Order Parameter R
    complex_sum = sum(cmath.rect(1.0, cmath.phase(z)) for z in Z) / nodes
    R = abs(complex_sum)
    Psi = cmath.phase(complex_sum)
    
    print("=== Z = Z^2 + C KURAMOTO MATRIX REPORT ===")
    print(f"Nodes (N)          : {nodes}")
    print(f"Control Parameter c : {c_val}")
    print(f"Order Parameter (R) : {R:.6f}")
    print(f"Mean Phase Angle Psi: {Psi:.6f} rad")
    print(f"State Convergence   : {'PHASE-LOCKED' if R > 0.8 else 'CHAOTIC DIVERGENCE'}")

if __name__ == "__main__":
    compute_z2_c_kuramoto()
