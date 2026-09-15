import binascii
import json
import struct
import time
import qrcode
import merkle_canon_dag

def build_unified_bridge():
    print("\033[1;35m================================================================\033[0m")
    print("\033[1;35m   UNIFIED DUAL-MODE OPTICAL & CONTACTLESS STATE BRIDGE ENGINE  \033[0m")
    print("\033[1;35m================================================================\033[0m")

    # 1. Fetch live Merkle Canon DAG root hash
    dag = merkle_canon_dag.dag
    root_node = next(n for n in dag.nodes.values() if n.node_id == "CANON_ROOT")
    dag_root_bytes = binascii.unhexlify(root_node.hash)

    # 2. Construct 78-Byte Binary Payload (Used for raw NFC writing)
    magic = b'K1'                                  # Protocol identifier (2 Bytes)
    epoch_time = int(time.time())                 # Epoch timestamp (4 Bytes)
    r_x13 = 1.0                                   # Coherence metric (4 Bytes Float32)
    tr_sigma = 1.2949e-15                         # Trace metric (4 Bytes Float32)
    sig_hash = binascii.unhexlify("e14f9a8d"*8)[:32]  # State signature (32 Bytes)

    header_pack = struct.pack(">2sIff", magic, epoch_time, r_x13, tr_sigma)
    binary_payload = header_pack + dag_root_bytes + sig_hash
    b64_payload = binascii.b2a_base64(binary_payload).decode('utf-8').strip()

    # 3. Export raw binary for NFC hardware tools
    with open("kuramoto_nfc_state.bin", "wb") as f:
        f.write(binary_payload)

    # 4. Build JSON Payload containing Base64 NFC Payload + Human Readable Telemetry for QR
    qr_payload = {
        "bridge": "OPTICAL_NFC_UNIFIED",
        "raw_b64": b64_payload,
        "telemetry": {
            "R_x13": r_x13,
            "Tr_Sigma": "1.2949e-15",
            "DAG_Root": root_node.hash
        }
    }
    serialized_qr = json.dumps(qr_payload, separators=(',', ':'))

    print(f"[+] Binary Payload Size : {len(binary_payload)} Bytes")
    print(f"[+] QR Serialized Size  : {len(serialized_qr)} Bytes")
    print(f"[+] Active DAG Root     : {root_node.hash[:16]}...")
    print("----------------------------------------------------------------")

    # 5. Generate and render QR Code
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=1,
        border=2
    )
    qr.add_data(serialized_qr)
    qr.make(fit=True)

    print("\033[1;37m")
    qr.print_ascii(invert=True)
    print("\033[0m----------------------------------------------------------------")

    # Save PNG Image
    img = qr.make_image(fill_color="black", back_color="white")
    img.save("state_proof_qr.png")

    print("\033[1;32m[✓] NFC BINARY GENERATED : ./kuramoto_nfc_state.bin\033[0m")
    print("\033[1;32m[✓] QR IMAGE GENERATED   : ./state_proof_qr.png\033[0m")
    print("\033[1;35m================================================================\033[0m")

if __name__ == "__main__":
    build_unified_bridge()
