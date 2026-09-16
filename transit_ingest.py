import hashlib
import json
import time

def simulate_live_transit_feed():
    # Simulating a live GTFS-Realtime data packet ingestion from transit feeds
    live_packet = {
        "source": "AU_TRIPVIEW_GTFS_REALTIME",
        "timestamp": int(time.time()),
        "vehicle_id": "TFS-SYD-720",
        "status": "IN_TRANSIT",
        "coordinates": {"lat": -33.8688, "lon": 151.2093}
    }
    
    raw_data = json.dumps(live_packet, sort_keys=True).encode("utf-8")
    transit_hash = hashlib.sha512(raw_data).hexdigest()
    
    print("===================================================")
    print("  [TRANSIT LAYER] : LIVE GTFS STREAM ANCHORED")
    print("===================================================")
    print(f"Transit Hash  : {transit_hash[:32]}...")
    print("===================================================")

if __name__ == "__main__":
    simulate_live_transit_feed()
