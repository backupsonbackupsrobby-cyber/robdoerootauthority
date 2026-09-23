import time
import hashlib

SECRET_KEY = "esp32"

def transmit_rf_frame(channel_freq, node_id, coherence):
    payload = f"NODE:{node_id}|FREQ:{channel_freq}|COH:{coherence:.6f}|SEC:{SECRET_KEY}"
    frame_hash = hashlib.sha256(payload.encode()).hexdigest()[:16]
    print(f"[RF-TX] Ch: {channel_freq}MHz | Node: {node_id} | Frame Hash: {frame_hash}")

if __name__ == "__main__":
    print(f"[*] Initializing RF Line Protocol via secret: {SECRET_KEY.upper()}")
    # Simulated multi-channel RF frequency hops for emergency/mesh grid
    channels = [915.0, 868.0, 433.5, 2412.0]
    
    for i, ch in enumerate(channels):
        transmit_rf_frame(ch, node_id=i+1, coherence=0.996000)
        time.sleep(0.1)
    
    print("[+] RF Lines Synchronized. Transceivers locked to frequency matrix.")
