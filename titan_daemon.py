import time
import subprocess

print("[DAEMON] Titan-Core background loop initiated...")
while True:
    subprocess.run(["python3", "termux_bridge.py"])
    time.sleep(10)
