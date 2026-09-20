import hashlib
import cmath

def sovereign_fractal_hash(c_val, max_iterations=129600):
    z = 0j
    for i in range(max_iterations):
        z = (z ** 2) + c_val
        if (z.real ** 2 + z.imag ** 2) > 4.0:
            break
            
    payload = f"Z_FINAL:{z.real:.6f}+{z.imag:.6f}_ITER:{i}_C:{c_val}"
    return hashlib.sha256(payload.encode()).hexdigest()

if __name__ == "__main__":
    c = complex(-0.75, 0.11)
    root_hash = sovereign_fractal_hash(c)
    print(f"ROOT-HASH-HEX: {root_hash}")
