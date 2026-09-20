import json
import os
import socket
import time

def pure_termux_bridge():
    ledger_file = "STATE_PROOFS.jsonl"
    latest = {}
    if os.path.exists(ledger_file):
        with open(ledger_file, "r") as f:
            lines = f.readlines()
            if lines:
                try:
                    latest = json.loads(lines[-1].strip())
                except Exception:
                    pass
    
    packet = {
        "node": "ATOM-TRUTH",
        "env": "Termux-Android",
        "epoch": int(time.time()),
        "ledger_tip": latest
    }
    
    serialized = json.dumps(packet)
    print("[PURE-TERMUX] Broadcast Packet:", serialized)
    
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        s.sendto(serialized.encode(), ("255.255.255.255", 8888))
        s.close()
        print("[SUCCESS] Packet sent over local network socket.")
    except Exception as e:
        print("[INFO] Local socket broadcast bypassed:", e)

if __name__ == "__main__":
    pure_termux_bridge()
