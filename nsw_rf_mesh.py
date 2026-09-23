import time
import hashlib

SECRET_KEY = "esp32"

def transmit_nsw_frame(channel_freq, node_id):
    payload = f"REGION:NSW-Edge|NODE:{node_id}|FREQ:{channel_freq}|SEC:{SECRET_KEY}"
    frame_hash = hashlib.sha256(payload.encode()).hexdigest()[:16]
    print(f"[MESH-TX] Region: NSW-Edge | Ch: {channel_freq}MHz | Node: {node_id} | Hash: {frame_hash}")

if __name__ == "__main__":
    print(f"[*] Initializing NSW Sovereign RF Line Protocol...")
    channels = [915.0, 868.0, 433.5, 2412.0]
    
    for i, ch in enumerate(channels, start=13):
        transmit_nsw_frame(ch, i)
        time.sleep(0.05)
        
    print("[+] NSW-Edge Transceiver Matrix Locked.")
    print("[+] Complete National Mesh Topology Synchronized.")
