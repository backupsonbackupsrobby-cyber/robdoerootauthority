import os, sys
if len(sys.argv) < 2:
    print("Error: No file descriptor passed.")
    sys.exit(1)

fd = int(sys.argv[1])
print(f"[*] Connected to USB file descriptor {fd}. Listening...")

try:
    while True:
        data = os.read(fd, 1024)
        if data:
            sys.stdout.buffer.write(data)
            sys.stdout.buffer.flush()
except Exception as e:
    print(f"\n[!] Error: {e}")
