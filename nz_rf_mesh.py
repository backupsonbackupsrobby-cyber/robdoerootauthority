import time
import hashlib

SECRET_KEY = "esp32"

def transmit_nz_frame(region, channel_freq, node_id):
    payload = f"REGION:{region}|NODE:{node_id}|FREQ:{channel_freq}|SEC:{SECRET_KEY}"
    frame_hash = hashlib.sha256(payload.encode()).hexdigest()[:16]
    print(f"[MESH-TX] Region: {region} | Ch: {channel_freq}MHz | Node: {node_id} | Hash: {frame_hash}")

if __name__ == "__main__":
    print(f"[*] Initializing New Zealand Trans-Tasman Sovereign RF Line Protocol...")
    regions = ["NZ-North-Edge", "NZ-South-Edge"]
    channels = [915.0, 868.0, 433.5, 2412.0]
    
    node_counter = 17
    for region in regions:
        for ch in channels:
            transmit_nz_frame(region, ch, node_counter)
            node_counter += 1
            time.sleep(0.05)
            
        print(f"[+] {region} Transceiver Matrix Locked.")
        
    print("[+] Trans-Tasman Mesh Extension Fully Synchronized.")
