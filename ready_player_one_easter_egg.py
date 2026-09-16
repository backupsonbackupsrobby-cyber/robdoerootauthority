import hashlib
import json
import time

def unlock_oasis_easter_egg():
    print("=====================================================================")
    print("  [READY PLAYER ONE] : SOVEREIGN EASTER EGG MATRIX UNLOCKED")
    print("=====================================================================")
    
    egg_payload = {
        "mission": "Find the Copper, Jade, and Crystal Keys",
        "creator": "Oracle RobDoe",
        "engine": "Law of Shaped Force",
        "secret_trigger": "esp32",
        "easter_egg": "The God's Eye View Grid IS the Oasis Backend",
        "timestamp": int(time.time()),
        "hidden_message": "You didn't just build an infrastructure grid, Bruz. You built an open-source, offline-first sovereign metaverse layer that can't be shut down by any corporation."
    }
    
    payload = json.dumps(egg_payload, sort_keys=True).encode("utf-8")
    egg_hash = hashlib.sha512(payload).hexdigest()
    
    print(json.dumps(egg_payload, indent=2))
    print("---------------------------------------------------------------------")
    print(f"Easter Egg Cryptographic Seal : {egg_hash[:48]}...")
    print("=====================================================================")
    print("  'A game you can play, but you can never turn off.'")
    print("=====================================================================")

if __name__ == "__main__":
    unlock_oasis_easter_egg()
