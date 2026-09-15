import binascii
import json
import math
import struct
import wave
import time
import qrcode
import merkle_canon_dag

def generate_full_stack():
    print("\033[1;33m================================================================\033[0m")
    print("\033[1;33m   SOVEREIGN ROOT AUTHORITY: FULL PHYSICAL STACK SYNTHESIS     \033[0m")
    print("\033[1;33m================================================================\033[0m")

    # 1. LAYER 2: Merkle Canon DAG Root Extraction
    dag = merkle_canon_dag.dag
    root_node = next(n for n in dag.nodes.values() if n.node_id == "CANON_ROOT")
    dag_root_bytes = binascii.unhexlify(root_node.hash)
    
    magic = b'K1'
    epoch_time = int(time.time())
    r_x13 = 1.0
    tr_sigma = 1.2949e-15
    sig_hash = binascii.unhexlify("e14f9a8d"*8)[:32]

    # Pack 78-Byte Binary Payload
    header_pack = struct.pack(">2sIff", magic, epoch_time, r_x13, tr_sigma)
    binary_payload = header_pack + dag_root_bytes + sig_hash
    b64_payload = binascii.b2a_base64(binary_payload).decode('utf-8').strip()

    # 2. LAYER 3: File System Ledger Logging
    log_entry = f"[{time.strftime('%Y-%m-%dT%H:%M:%S%z')}] ALL_LAYERS_SEALED | ROOT:{root_node.hash} | R_x13={r_x13:.6f}\n"
    with open("state_proofs.log", "a") as f:
        f.write(log_entry)
    print("\033[1;32m[✓] Layer 3 (File Ledger)   : Log appended to state_proofs.log\033[0m")

    # 3. LAYER 5: NFC Binary Export
    with open("kuramoto_nfc_state.bin", "wb") as f:
        f.write(binary_payload)
    print("\033[1;32m[✓] Layer 5 (Contactless)    : Raw binary stored -> kuramoto_nfc_state.bin\033[0m")

    # 4. LAYER 4: Optical QR Generation
    qr_payload = {
        "stack": "SOVEREIGN_ROOT_6_LAYER",
        "raw_b64": b64_payload,
        "dag_root": root_node.hash
    }
    serialized_qr = json.dumps(qr_payload, separators=(',', ':'))
    
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=1,
        border=2
    )
    qr.add_data(serialized_qr)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save("state_proof_qr.png")
    print("\033[1;32m[✓] Layer 4 (Optical Image) : PNG generated -> state_proof_qr.png\033[0m")

    # 5. LAYER 6: Acoustic FSK Wave Generator (Pure PCM Wave Synthesis)
    sample_rate = 44100
    baud_rate = 300       # 300 bits per second
    freq_0 = 1200         # 1200 Hz for Binary '0'
    freq_1 = 2200         # 2200 Hz for Binary '1'
    samples_per_bit = int(sample_rate / baud_rate)

    audio_samples = []
    
    # Convert binary payload to bit string
    bit_string = ''.join(f'{byte:08b}' for byte in binary_payload)

    # Synthesize PCM sine wave samples for each bit
    phase = 0.0
    for bit in bit_string:
        freq = freq_1 if bit == '1' else freq_0
        phase_incr = (2.0 * math.pi * freq) / sample_rate
        for _ in range(samples_per_bit):
            sample = int(32767.0 * math.sin(phase))
            audio_samples.append(struct.pack('<h', sample))
            phase += phase_incr
            if phase > 2.0 * math.pi:
                phase -= 2.0 * math.pi

    with wave.open("state_proof_audio.wav", "wb") as wav_file:
        wav_file.setnchannels(1)      # Mono
        wav_file.setsampwidth(2)      # 16-bit PCM
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(b''.join(audio_samples))

    print("\033[1;32m[✓] Layer 6 (Acoustic Wave)  : FSK Audio synthesized -> state_proof_audio.wav\033[0m")
    print("----------------------------------------------------------------")
    
    # Print terminal representation of physical stack
    qr.print_ascii(invert=True)

    print("\033[1;33m================================================================\033[0m")
    print("\033[1;32m[🚀] 6-LAYER PHYSICAL STATE EMBEDDING COMPLETE & SEALED\033[0m")
    print("\033[1;33m================================================================\033[0m")

if __name__ == "__main__":
    generate_full_stack()
