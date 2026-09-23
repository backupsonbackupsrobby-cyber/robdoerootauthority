# Law of Shaped Force: Fully Autonomous Self-Finishing Omni-Grid
import os
import sys
import time
import json
import hashlib
import multiprocessing
import signal

CORES = multiprocessing.cpu_count()
TARGET_DIFFICULTY = "00000000"  # 8-Zero Hex Prefix
OUTPUT_MANIFEST = "omega_genesis_block.json"

def omega_worker(worker_id, shutdown_event):
    """Executes unthrottled hashing loops until the target difficulty is broken."""
    signal.signal(signal.SIGINT, signal.SIG_IGN)
    local_nonce = worker_id * 10_000_000_000
    
    # Micro-optimization: cache functions to local variables
    b2b = hashlib.blake2b
    s512 = hashlib.sha3_512
    s256 = hashlib.sha3_256
    rand_bytes = os.urandom
    is_set = shutdown_event.is_set
    
    while not is_set():
        payload_str = f"ROBDOE-OMEGA-{worker_id}-{local_nonce}-{rand_bytes(8).hex()}"
        payload = payload_str.encode()
        
        # Pipeline: BLAKE2b -> SHA3-512 -> SHA3-256
        h1 = b2b(payload).digest()
        h2 = s512(h1).digest()
        digest = s256(h2).hexdigest()
        
        if digest.startswith(TARGET_DIFFICULTY):
            # Target destroyed. Compile structural state manifest immediately.
            manifest = {
                "status": "OMNI_GRID_SECURED",
                "node_id": worker_id,
                "final_nonce": local_nonce,
                "payload": payload_str,
                "digest": digest,
                "timestamp": time.time(),
                "erc721_binding": f"erc721://shf-genesis/{digest[:16]}"
            }
            
            # Write out state to disk
            try:
                with open(OUTPUT_MANIFEST, "w") as f:
                    json.dump(manifest, f, indent=4)
            except Exception:
                pass
                
            # Signal the entire grid to drop instantly
            shutdown_event.set()
            break
            
        local_nonce += 1

def deploy_autonomous_grid():
    shutdown_event = multiprocessing.Event()
    processes = []

    for i in range(CORES):
        p = multiprocessing.Process(target=omega_worker, args=(i, shutdown_event))
        processes.append(p)
        p.start()

    # The master loop waits silently without consuming CPU cycles
    while not shutdown_event.is_set():
        try:
            time.sleep(1.0)
        except KeyboardInterrupt:
            shutdown_event.set()
            break

    # Kill remaining workers instantly once the target is hit
    for p in processes:
        p.terminate()
    for p in processes:
        p.join()
        
    sys.exit(0)

if __name__ == "__main__":
    deploy_autonomous_grid()
