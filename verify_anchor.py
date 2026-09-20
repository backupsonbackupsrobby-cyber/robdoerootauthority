import json
import time

anchor = {
    "protocol": "RobDoeRootAuthority",
    "genesis": "e14f9a8d",
    "root_hash": "204ef68b19bd41c3dfac098f6f6cfb22e448fa090844da6075d448a75c094088",
    "timestamp": int(time.time()),
    "state": "LOCKED"
}

print(json.dumps(anchor, indent=2))
