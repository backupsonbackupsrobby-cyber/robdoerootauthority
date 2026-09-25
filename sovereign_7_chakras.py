import hashlib
import json
import subprocess
import time

def generate_7_chakras_registry():
    print("[*] Encoding 7 Chakras internal sovereign tags and root hash hex...")
    
    chakras = [
        {"id": 1, "name": "Muladhara", "focus": "Root / Foundation", "tag": "ATOM-CHAKRA-1-ROOT"},
        {"id": 2, "name": "Svadhisthana", "focus": "Sacral / Flow", "tag": "ATOM-CHAKRA-2-SACRAL"},
        {"id": 3, "name": "Manipura", "focus": "Solar Plexus / Will", "tag": "ATOM-CHAKRA-3-SOLAR"},
        {"id": 4, "name": "Anahata", "focus": "Heart / Balance", "tag": "ATOM-CHAKRA-4-HEART"},
        {"id": 5, "name": "Vishuddha", "focus": "Throat / Expression", "tag": "ATOM-CHAKRA-5-THROAT"},
        {"id": 6, "name": "Ajna", "focus": "Third Eye / Vision", "tag": "ATOM-CHAKRA-6-VISION"},
        {"id": 7, "name": "Sahasrara", "focus": "Crown / Sovereign Unity", "tag": "ATOM-CHAKRA-7-CROWN"}
    ]
    
    chakra_records = []
    combined_hash_input = ""
    
    for c in chakras:
        payload = f"{c['tag']}-RobDoePtyLtd"
        h = hashlib.sha512(payload.encode('utf-8')).hexdigest()
        chakra_records.append({
            "chakra_id": c["id"],
            "name": c["name"],
            "focus": c["focus"],
            "internal_tag": c["tag"],
            "sha512_hash": h
        })
        combined_hash_input += h
        
    master_root_hex = hashlib.sha512(combined_hash_input.encode('utf-8')).hexdigest()
    
    registry = {
        "protocol": "ATOM-TRUTH-7-CHAKRAS-SOVEREIGN-REGISTRY",
        "authority": "RobDoe Pty Ltd",
        "master_root_hash": master_root_hex,
        "chakras": chakra_records,
        "timestamp": time.time()
    }
    
    with open("sovereign_7_chakras_registry.json", "w", encoding="utf-8") as f:
        json.dump(registry, f, indent=4)
        
    print(f"[+] 7 Chakras Master Root Hash Hex Locked: {master_root_hex}")
    return master_root_hex

if __name__ == "__main__":
    r_hash = generate_7_chakras_registry()
    subprocess.run(["git", "add", "sovereign_7_chakras_registry.json"], check=True)
    commit_msg = f"chakras(master): {r_hash[:32]} - 7 Chakras internal tags & root hash hex locked"
    subprocess.run(["git", "commit", "-m", commit_msg], check=True)
    result = subprocess.run(["git", "push", "origin", "main"], capture_output=True, text=True)
    if result.returncode != 0:
        subprocess.run(["git", "push", "origin", "master"], capture_output=True, text=True)
    print(f"[+] SUCCESS: 7 Chakras Sovereign Registry Pushed Live! Hash: {r_hash}")
