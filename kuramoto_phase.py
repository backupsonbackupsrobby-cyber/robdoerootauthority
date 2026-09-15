import numpy as np
import subprocess
import hashlib

objs = [l.split()[0] for l in subprocess.check_output(['git', 'rev-list', '--all', '--objects']).decode().strip().split('\n') if l]
N = len(objs)
h_vals = [hashlib.sha512(o.encode()).digest() for o in objs]
theta = np.array([(int.from_bytes(h[:4], 'big') / (2**32-1)) * 2 * np.pi for h in h_vals])
omega = np.array([0.5 + (int.from_bytes(h[4:8], 'big') / (2**32-1)) for h in h_vals])
K, dt = 2.5, 0.05

print('================================================================')
print(f'   KURAMOTO PHASE COUPLING ENGINE | TARGET LEAVES: {N}')
print('================================================================')

for t in range(10):
    Z = np.mean(np.exp(1j * theta))
    R, psi = np.abs(Z), np.angle(Z)
    print(f'Step {t+1:02d} | Objects: {N} | Order Parameter R = {R:.6f} | Phase Psi = {psi:.4f} rad')
    theta = (theta + (omega + K * R * np.sin(psi - theta)) * dt) % (2 * np.pi)

print('================================================================')
print(f'FINAL COHERENCE LOCK: R = {R:.6f}')
