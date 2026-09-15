import struct
import time
import binascii
import merkle_canon_dag

def generate_nfc_binary():
    print("\033[1;36m================================================================\033[0m")
    print("\033[1;36m       KURAMOTO 13D NFC NDEF STATE ENCODING ENGINE              \033[0m")
    print("\033[1;36m================================================================\033[0m")

    # 1. Fetch live Merkle Canon DAG root hash
    dag = merkle_canon_dag.dag
    root_node = next(n for n in dag.nodes.values() if n.node_id == "CANON_ROOT")
    dag_root_bytes = binascii.unhexlify(root_node.hash)

    # 2. Extract telemetry invariants
    magic = b'K1'                                 # 2 Bytes: Header Identifier
    epoch_time = int(time.time())                # 4 Bytes: Timestamp uint32
    r_x13 = 1.0                                  # 4 Bytes: Float32 Coherence
    tr_sigma = 1.2949e-15                        # 4 Bytes: Float32 Covariance
    sig_hash = binascii.unhexlify("e14f9a8d"*8)[:32] # 32 Bytes: State Signature

    # 3. Pack struct into 78-byte binary stream
    header_pack = struct.pack(">2sIff", magic, epoch_time, r_x13, tr_sigma)
    nfc_payload = header_pack + dag_root_bytes + sig_hash

    # 4. Save to binary payload file
    with open("kuramoto_nfc_state.bin", "wb") as f:
        f.write(nfc_payload)

    payload_hex = binascii.hexlify(nfc_payload).decode('utf-8')

    print(f"[+] Total Binary Size : {len(nfc_payload)} Bytes")
    print(f"[+] Magic Header      : {magic.decode('utf-8')}")
    print(f"[+] Order Metric R_x13: {r_x13}")
    print(f"[+] Merkle Root Hex   : {root_node.hash[:16]}...")
    print(f"[+] Payload Hex Dump  : {payload_hex}")
    print("----------------------------------------------------------------")
    print("\033[1;32m[✓] NFC BINARY PAYLOAD WRITTEN TO: kuramoto_nfc_state.bin\033[0m")
    print("\033[1;36m================================================================\033[0m")

if __name__ == "__main__":
    generate_nfc_binary()
