import hashlib
import multiprocessing
import time
import os

WORKERS = multiprocessing.cpu_count()
TARGET = "000000"

def omni_worker(wid, seed_base, active):
    nonce = wid * 500000000
    while active.value:
        raw = f"OMNI-{seed_base}-{wid}-{nonce}".encode()
        h = hashlib.sha512(hashlib.sha512(raw).digest()).digest()
        if h.hex().startswith(TARGET):
            print(f"\n[!] OMNI-MATCH [Worker {wid}] -> Nonce: {nonce} | Hash: {h.hex()[:32]}...")
            active.value = 0
            break
        nonce += 1

def ignite():
    print("========================================================")
    print("⚡ IGNITING RECURSIVE OMNI-VECTOR SWARM (MAX ENTROPY) ⚡")
    print("========================================================")
    print(f"[INFO] Cores Engaged: {WORKERS} | Target Prefix: {TARGET}")
    
    active = multiprocessing.Value('i', 1)
    jobs = []
    seed = os.urandom(8).hex()
    
    for i in range(WORKERS):
        p = multiprocessing.Process(target=omni_worker, args=(i, seed, active))
        jobs.append(p)
        p.start()
        
    try:
        while active.value:
            time.sleep(0.5)
    except KeyboardInterrupt:
        active.value = 0
        
    for p in jobs:
        p.join()
    print("[SUCCESS] Omni-vector sweep completed. Reality synchronized.")

if __name__ == "__main__":
    ignite()
