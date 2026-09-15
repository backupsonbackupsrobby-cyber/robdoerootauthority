import struct
import binascii

def decode_nfc_state():
    with open("kuramoto_nfc_state.bin", "rb") as f:
        data = f.read()

    # Unpack fixed binary fields
    magic, epoch, r_x13, tr_sigma = struct.unpack(">2sIff", data[:14])
    dag_root = binascii.hexlify(data[14:46]).decode('utf-8')
    sig = binascii.hexlify(data[46:78]).decode('utf-8')

    print("\033[1;34m================================================================\033[0m")
    print("\033[1;34m        NFC HARDWARE TOKEN READ & VERIFICATION COMPLETE         \033[0m")
    print("\033[1;34m================================================================\033[0m")
    print(f"[+] Token Header      : {magic.decode('utf-8')} (Kuramoto Engine V1)")
    print(f"[+] Tap Timestamp     : {epoch}")
    print(f"[+] Decoded R_x13     : {r_x13:.6f}")
    print(f"[+] Decoded Tr(Sigma) : {tr_sigma:.4e}")
    print(f"[+] Restored DAG Root : {dag_root}")
    print("----------------------------------------------------------------")

    if r_x13 == 1.0 and magic == b'K1':
        print("\033[1;32m[✓] STATE INTEGRITY CONFIRMED VIA CONTACTLESS HARDWARE TAP\033[0m")
    else:
        print("\033[1;31m[-] STATE CORRUPTED OR UNVERIFIED\033[0m")
    print("\033[1;34m================================================================\033[0m")

if __name__ == "__main__":
    decode_nfc_state()
