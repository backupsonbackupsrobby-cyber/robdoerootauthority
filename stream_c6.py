cat << 'EOF' > stream_c6.py
import sys
import os
import usb.core
import usb.backend.libusb1

if len(sys.argv) < 2:
    print("Usage: python3 stream_c6.py <descriptor_number>")
    sys.exit(1)

fd = int(sys.argv[1])

# Initialize libusb backend and wrap the termux-usb file descriptor
backend = usb.backend.libusb1.get_backend()
lib = backend.lib

lib.libusb_wrap_sys_device.argtypes = [
    backend.libusb_context_p,
    libusb1_c_int := int, # handled via ctypes
    backend.libusb_device_handle_pp
]

# Alternative straightforward fd wrap using standard low-level reading if endpoints are exposed:
print(f"[*] Initialized wrapper for FD {fd}. Reading raw bulk endpoints...")

try:
    # Read directly from the raw pass-through file descriptor as a binary stream 
    # by correctly targeting the underlying pipe/socket allocated by termux-usb
    with os.fdopen(fd, 'rb', buffering=0) as f:
        while True:
            data = f.read(64)
            if data:
                sys.stdout.buffer.write(data)
                sys.stdout.buffer.flush()
except Exception as e:
    print(f"\n[!] Stream Error: {e}")
EOF
