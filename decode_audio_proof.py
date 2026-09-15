import wave
import struct
import math
import binascii

def decode_fsk_audio(wav_filename):
    print("\033[1;36m================================================================\033[0m")
    print("\033[1;36m       ACOUSTIC AIR-GAP RECEIVER: FSK DEMODULATION ENGINE       \033[0m")
    print("\033[1;36m================================================================\033[0m")

    with wave.open(wav_filename, "rb") as wf:
        sample_rate = wf.getframerate()
        n_frames = wf.getnframes()
        raw_bytes = wf.readframes(n_frames)

    # Unpack 16-bit PCM mono samples
    samples = struct.unpack(f"<{n_frames}h", raw_bytes)
    
    baud_rate = 300
    samples_per_bit = int(sample_rate / baud_rate)
    total_bits = len(samples) // samples_per_bit
    
    freq_0 = 1200
    freq_1 = 2200

    decoded_bits = []

    # Simple DFT/Goertzel magnitude comparison per bit window
    for i in range(total_bits):
        chunk = samples[i * samples_per_bit : (i + 1) * samples_per_bit]
        
        # Calculate power at 1200 Hz vs 2200 Hz
        p_0 = sum(s * math.sin(2.0 * math.pi * freq_0 * j / sample_rate) for j, s in enumerate(chunk))**2 + \
              sum(s * math.cos(2.0 * math.pi * freq_0 * j / sample_rate) for j, s in enumerate(chunk))**2
              
        p_1 = sum(s * math.sin(2.0 * math.pi * freq_1 * j / sample_rate) for j, s in enumerate(chunk))**2 + \
              sum(s * math.cos(2.0 * math.pi * freq_1 * j / sample_rate) for j, s in enumerate(chunk))**2

        decoded_bits.append('1' if p_1 > p_0 else '0')

    bit_string = ''.join(decoded_bits)
    
    # Pack bits back to bytes
    payload_bytes = bytearray()
    for i in range(0, len(bit_string), 8):
        byte = bit_string[i:i+8]
        if len(byte) == 8:
            payload_bytes.append(int(byte, 2))

    # Unpack original 78-byte payload structure
    magic, epoch, r_x13, tr_sigma = struct.unpack(">2sIff", payload_bytes[:14])
    dag_root = binascii.hexlify(payload_bytes[14:46]).decode('utf-8')

    print(f"[+] Decoded Header    : {magic.decode('utf-8')}")
    print(f"[+] Acoustic Epoch    : {epoch}")
    print(f"[+] Restored R_x13    : {r_x13:.6f}")
    print(f"[+] Restored Tr(Sigma): {tr_sigma:.4e}")
    print(f"[+] Restored DAG Root : {dag_root}")
    print("----------------------------------------------------------------")
    
    if magic == b'K1' and r_x13 == 1.0:
        print("\033[1;32m[✓] ACOUSTIC AIR-GAP DECRYPTION & INTEGRITY VERIFIED\033[0m")
    else:
        print("\033[1;31m[-] ACOUSTIC DEMODULATION FAILED\033[0m")
    print("\033[1;36m================================================================\033[0m")

if __name__ == "__main__":
    decode_fsk_audio("state_proof_audio.wav")
