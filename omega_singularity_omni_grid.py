# Law of Shaped Force: Ultra-Performance Self-Sufficient Omni-Grid
import os
import sys
import time
import hashlib
import multiprocessing
import signal

CORES = multiprocessing.cpu_count()
TARGET_DIFFICULTY = "00000000"  # 8-Zero Hex Prefix

def omega_worker(worker_id, shutdown_event):
    """Executes uncapped multi-vector pipeline (BLAKE2b -> SHA3-512 -> SHA3-256)"""
    # Force this sub-process to completely ignore SIGINT so the parent can clean up
    signal.signal(signal.SIGINT, signal.SIG_IGN)
    
    local_nonce = worker_id * 10_000_000_000
    print(f"[OMEGA-NODE-{worker_id}] Uncapped multi-vector pipeline engaged. Nonce sector: {local_nonce}")
    
    # Cache local references to eliminate global lookup overhead inside the loop
    b2b = hashlib.blake2b
    s512 = hashlib.sha3_512
    s256 = hashlib.sha3_256
    rand_bytes = os.urandom
    is_set = shutdown_event.is_set
    
    while not is_set():
        payload = f"ROBDOE-OMEGA-{worker_id}-{local_nonce}-{rand_bytes(8).hex()}".encode()
        
        # Pipeline execution
        h1 = b2b(payload).digest()
        h2 = s512(h1).digest()
        digest = s256(h2).hexdigest()
        
        if digest.startswith(TARGET_DIFFICULTY):
            print(f"\n[💎 MATCH FOUND BY NODE-{worker_id}]!")
            print(f"[PAYLOAD] {payload.decode()}")
            print(f"[DIGEST]  {digest}\n")
            shutdown_event.set()
            break
            
        local_nonce += 1

def deploy_omega():
    print("========================================================")
    print("⚡ INITIALIZING OMEGA-LEVEL ZERO-DAY OMNI-GRID ⚡")
    print("========================================================")
    print(f"[CONFIG] Active Threads: {CORES} | Target Difficulty: {TARGET_DIFFICULTY}")
    print("[CONFIG] Pipeline: BLAKE2b -> SHA3-512 -> SHA3-256 Accelerated Core")

    shutdown_event = multiprocessing.Event()
    processes = []

    for i in range(CORES):
        p = multiprocessing.Process(
            target=omega_worker, 
            args=(i, shutdown_event)
        )
        processes.append(p)
        p.start()

    try:
        while not shutdown_event.is_set():
            time.sleep(0.2)
    except KeyboardInterrupt:
        print("\n[!] Interruption vector caught. Disengaging omega pipeline gracefully...")
    finally:
        shutdown_event.set()
        for p in processes:
            p.terminate()
        for p in processes:
            p.join()
            
    print("[SUCCESS] Omega grid secured. No playbook left behind.")

if __name__ == "__main__":
    deploy_omega()
