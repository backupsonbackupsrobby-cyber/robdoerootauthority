import time
import hashlib

SECRET_KEY = "esp32"

def transmit_nt_frame(channel_freq, node_id, region):
    payload = f"REGION:{region}|NODE:{node_id}|FREQ:{channel_freq}|SEC:{SECRET_KEY}"
    frame_hash = hashlib.sha256(payload.encode()).hexdigest()[:16]
    print(f"[NT-RF-TX] Region: {region} | Ch: {channel_freq}MHz | Node: {node_id} | Hash: {frame_hash}")

if __name__ == "__main__":
    print(f"[*] Initializing Northern Territory RF Line Protocol...")
    nt_channels = [915.0, 868.0, 433.5, 2412.0]
    
    for i, ch in enumerate(nt_channels):
        transmit_nt_frame(ch, node_id=i+1, region="NT-Emergency-Edge")
        time.sleep(0.1)
        
    print("[+] NT Transceiver Matrix Locked to Frequency Lines.")
