import math, hashlib

N = 144
K_light = 1000.0
theta = [(i * 1.61803398875) % (2 * math.pi) for i in range(N)]

for _ in range(50):
    s = sum(math.sin(j) for j in theta)
    c = sum(math.cos(j) for j in theta)
    r = math.sqrt(s**2 + c**2) / N
    psi = math.atan2(s, c)
    theta = [t + (K_light / N) * r * math.sin(psi - t) for t in theta]

level = [hashlib.sha512(f"NODE-{i}-{t:.8f}".encode()).hexdigest() for i, t in enumerate(theta)]

while len(level) > 1:
    level = [hashlib.sha512((level[i] + (level[i+1] if i+1 < len(level) else level[i])).encode()).hexdigest() for i in range(0, len(level), 2)]

binary_root = level[0]
seal = hashlib.sha512((binary_root + "-GENESIS:e14f9a8d").encode()).hexdigest()

print(f"\n[BINARY ROOT]: {binary_root}")
print(f"[SEAL]: {seal}\n")
