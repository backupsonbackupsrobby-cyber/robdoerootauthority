import sys
import json
import subprocess
import math
import cmath
import random
import hashlib

def compute_order_parameter(phases):
    """Compute Kuramoto order parameter R (coherence) and average phase psi."""
    N = len(phases)
    complex_sum = sum(cmath.exp(1j * theta) for theta in phases)
    complex_order = complex_sum / N
    R = abs(complex_order)
    psi = cmath.phase(complex_order)
    return R, psi

def run_kuramoto_step(phases, omegas, K=8.0, dt=0.05):
    """Step oscillator phases forward with strong coupling K."""
    N = len(phases)
    new_phases = []
    two_pi = 2 * math.pi
    
    for i in range(N):
        interaction = sum(math.sin(phases[j] - phases[i]) for j in range(N))
        d_phase = omegas[i] + (K / N) * interaction
        updated_phase = (phases[i] + d_phase * dt) % two_pi
        new_phases.append(updated_phase)
        
    return new_phases

def compute_merkle_leaf(R, psi, signal):
    """Hash the order parameter R, mean phase psi, and signal into a SHA-256 state leaf."""
    payload = f"SIGNAL:{signal}|R:{R:.6f}|PSI:{psi:.6f}".encode('utf-8')
    return hashlib.sha256(payload).hexdigest()

def scan_nfc_payload():
    print("Listening for NFC tag... (Tap tag to antenna)")
    try:
        result = subprocess.run(["termux-nfc", "-r", "short"], capture_output=True, text=True, timeout=15)
        raw_str = result.stdout.strip()
        
        if not raw_str:
            return None

        try:
            raw_data = json.loads(raw_str)
            if isinstance(raw_data, list) and len(raw_data) > 0:
                return str(raw_data[0].get("Payload") or raw_data[0].get("TagId") or "EMPTY_TAG")
            elif isinstance(raw_data, dict):
                return str(raw_data.get("Payload") or raw_data.get("TagId") or "EMPTY_TAG")
        except json.JSONDecodeError:
            return f"RAW_STRING:{raw_str}"

    except Exception:
        pass
    return None

if __name__ == "__main__":
    N_OSCILLATORS = 8
    K_COUPLING = 8.0  # Super-critical coupling for rapid phase locking
    STEPS = 20
    
    tag_input = sys.argv[1] if len(sys.argv) > 1 else (scan_nfc_payload() or "RAW:FALLBACK_NODE")
    
    random.seed(42)
    phases = [random.uniform(0, 2 * math.pi) for _ in range(N_OSCILLATORS)]
    omegas = [random.gauss(1.0, 0.05) for _ in range(N_OSCILLATORS)]
    
    phase_shift = (hash(tag_input) % 360) * (math.pi / 180.0)
    
    print("\n--- KURAMOTO PHASE COUPLING INITIATED ---")
    print(f"Signal Input: {tag_input}")
    print(f"Perturbation Delta: {phase_shift:.4f} rad\n")
    
    phases[0] = (phases[0] + phase_shift) % (2 * math.pi)
    
    for step in range(1, STEPS + 1):
        phases = run_kuramoto_step(phases, omegas, K=K_COUPLING, dt=0.05)
        R, psi = compute_order_parameter(phases)
        
        if step % 4 == 0 or step == STEPS:
            leaf = compute_merkle_leaf(R, psi, tag_input)
            print(f"Step {step:02d} | R = {R:.4f} | Psi = {psi:.4f} rad | SHA256 Leaf: {leaf[:16]}...")

