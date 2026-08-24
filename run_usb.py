cat << 'EOF' > run_usb.py
import sys
import os
import usb.core
import usb.backend.libusb1

if len(sys.argv) < 2:
    print("Error: No file descriptor provided.")
    sys.exit(1)

fd = int(sys.argv[1])
backend = usb.backend.libusb1.get_backend()
if not backend:
    print("Error: libusb backend not found.")
    sys.exit(1)

# Initialize libusb context and wrap the Termux-passed file descriptor
ctx = backend.context()
handle = backend.lib.libusb_wrap_sys_device(ctx.handle, fd)
if not handle:
    print("Error: Failed to wrap system device file descriptor.")
    sys.exit(1)

dev = usb.core.Device(handle, backend)
print(f"[*] Successfully attached to ESP32-C6! Vendor: {hex(dev.idVendor)}, Product: {hex(dev.idProduct)}")

# Find active configuration and endpoints for reading data
cfg = dev.get_active_configuration()
intf = cfg[(0,0)]

ep_in = None
for ep in intf:
    if usb.util.endpoint_direction(ep.bEndpointAddress) == usb.util.ENDPOINT_IN:
        ep_in = ep.bEndpointAddress
        break

if not ep_in:
    print("[!] Warning: No input endpoint found automatically.")
else:
    print(f"[*] Listening on Endpoint {hex(ep_in)}...")
    while True:
        try:
            data = dev.read(ep_in, 64, timeout=1000)
            if data:
                sys.stdout.buffer.write(bytes(data))
                sys.stdout.buffer.flush()
        except usb.core.USBError as e:
            if e.errno == 110: # Timeout
                continue
            else:
                break
EOF
