import time
import os
import subprocess

def run_loop():
    print("\033[1;36m[+] SOVEREIGN DAEMON INITIALIZED | LOOP INTERVAL: 360s\033[0m")
    while True:
        try:
            print(f"\n\033[1;32m[+] [{time.strftime('%Y-%m-%d %H:%M:%S')}] Executing Phase Synchronization...\033[0m")
            # Run non-destructive absorption and merkle indexing
            subprocess.run(["python3", "absorb_never_delete.py", "."], check=True)
        except Exception as e:
            print(f"\033[1;31m[-] Loop Error: {e}\033[0m")
        
        # Sleep for cyclic interval
        time.sleep(360)

if __name__ == "__main__":
    run_loop()
