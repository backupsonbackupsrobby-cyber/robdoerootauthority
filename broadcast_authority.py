import json
import time

def broadcast_genesis_state():
    vector_packet = {
        "protocol": "RobDoeRootAuthority",
        "genesis": "e14f9a8d",
        "root_hash": "204ef68b19bd41c3dfac098f6f6cfb22e448fa090844da6075d448a75c094088",
        "timestamp": int(time.time()),
        "state": "BROADCAST_LOCKED"
    }
    print("[ATOM-TRUTH] Broadcasting Sovereign State Packet...")
    print(json.dumps(vector_packet, indent=2))

if __name__ == "__main__":
    broadcast_genesis_state()
