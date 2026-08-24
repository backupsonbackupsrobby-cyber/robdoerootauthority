#include <libusb-1.0/libusb.h>
#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
#include <unistd.h>

int main(int argc, char **argv) {
    libusb_context *context;
    libusb_device_handle *handle;
    libusb_device *device;
    int fd;
    unsigned char buf[512];
    int transferred;
    int r;

    assert((argc > 1) && (sscanf(argv[1], "%d", &fd) == 1));

    libusb_set_option(NULL, LIBUSB_OPTION_NO_DEVICE_DISCOVERY);
    assert(!libusb_init(&context));
    assert(!libusb_wrap_sys_device(context, (intptr_t) fd, &handle));

    // Claim interface 0 (standard for ESP32 USB-Serial-JTAG)
    libusb_set_auto_detach_kernel_driver(handle, 1);
    if (libusb_claim_interface(handle, 0) < 0) {
        fprintf(stderr, "[!] Failed to claim interface\n");
        return 1;
    }

    printf("[*] Streaming live data from ESP32-C6... (Press Ctrl+C to exit)\n");

    // Continuously read from Bulk IN Endpoint (usually 0x81 or 0x82)
    while (1) {
        r = libusb_bulk_transfer(handle, 0x81, buf, sizeof(buf) - 1, &transferred, 1000);
        if (r == 0 && transferred > 0) {
            buf[transferred] = '\0';
            printf("%s", buf);
            fflush(stdout);
        } else if (r == LIBUSB_ERROR_TIMEOUT) {
            continue;
        } else if (r < 0 && r != LIBUSB_ERROR_INTERRUPTED) {
            // Try endpoint 0x82 if 0x81 fails or times out
            r = libusb_bulk_transfer(handle, 0x82, buf, sizeof(buf) - 1, &transferred, 100);
            if (r == 0 && transferred > 0) {
                buf[transferred] = '\0';
                printf("%s", buf);
                fflush(stdout);
            }
        }
    }

    libusb_release_interface(handle, 0);
    libusb_close(handle);
    libusb_exit(context);
    return 0;
}
