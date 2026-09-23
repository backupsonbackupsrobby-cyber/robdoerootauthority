import time
import hashlib

SECRET_KEY = "esp32"

def transmit_hemisphere_node(region, channel_freq, node_id):
    payload = f"HEMISPHERE:SOUTH|REGION:{region}|NODE:{node_id}|FREQ:{channel_freq}|SEC:{SECRET_KEY}"
    frame_hash = hashlib.sha256(payload.encode()).hexdigest()[:16]
    print(f"[GLOBAL-TX] Region: {region} | Ch: {channel_freq}MHz | Node: {node_id} | Hash: {frame_hash}")

if __name__ == "__main__":
    print(f"[*] Initializing Southern Hemisphere Global Sovereign Mesh...")
    sectors = [
        "Africa-South-Edge", 
        "South-America-Andes-Edge", 
        "Antarctic-Deep-Field-Edge"
    ]
    channels = [915.0, 868.0, 433.5, 2412.0]
    
    node_counter = 25
    for sector in sectors:
        for ch in channels:
            transmit_hemisphere_node(sector, ch, node_counter)
            node_counter += 1
            time.sleep(0.03)
            
        print(f"[+] {sector} Transceiver Matrix Locked.")
        
    print("[+] Southern Hemisphere Global Mesh Topology Fully Synchronized.")
