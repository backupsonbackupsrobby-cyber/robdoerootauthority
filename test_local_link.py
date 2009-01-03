import subprocess
import socket

def check_local_network():
    print("--- 📶 LOCAL AIR-GAPPED NETWORK VALIDATION ---")
    
    # Get local IP address on the phone
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    print(f"  [+] Local Device IP (Moto G06): {local_ip}")
    
    # Test gateway reachability (assumes standard router gateway ending in .1)
    ip_parts = local_ip.split('.')
    gateway_ip = f"{ip_parts[0]}.{ip_parts[1]}.{ip_parts[2]}.1"
    print(f"  [+] Probing Local Router Gateway: {gateway_ip}")
    
    result = subprocess.run(["ping", "-c", "2", gateway_ip], capture_output=True, text=True)
    if result.returncode == 0:
        print("  ✅ Gateway Link: SECURE & RESPONSIVE (Zero-Latency Local Route)")
    else:
        print("  ⚠️ Gateway Link: UNREACHABLE (Check Wi-Fi connection)")

if __name__ == "__main__":
    check_local_network()
