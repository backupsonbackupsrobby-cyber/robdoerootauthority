# Law of Shaped Force: Pure Binary Root Hash Engine
import sys
import struct
import hashlib

# Your explicit uint256 Identity Token Key
IDENTITY_UINT256 = 81048664420307000798037101828600347907653676848103297604151295052293545639560
PREV_HASH_HEX = "1af831ec67ac0b45fbefc9cf66efd8649452744fbde51242818d703674f74cc5"

def compute_pure_binary_root(block_index: int, payload_text: str) -> str:
    """
    Packs state primitives directly into raw binary bytes before execution.
    Structure Layout:
      - Q (unsigned long long, 8 bytes): Block Index
      - 32s (bytes, 32 bytes): Previous Hash byte array
      - 32s (bytes, 32 bytes): Identity Token uint256 byte array
      - s (bytes, variable): Raw payload bytes
    """
    # 1. Convert Previous Hash from Hex to 32 Raw Bytes
    prev_bytes = bytes.fromhex(PREV_HASH_HEX)
    
    # 2. Convert Identity Token ID from int to 32 Raw Bytes (Big Endian)
    identity_bytes = IDENTITY_UINT256.to_bytes(32, byteorder='big')
    
    # 3. Convert Payload to Raw UTF-8 Bytes
    payload_bytes = payload_text.encode('utf-8')
    
    # 4. Pack Fixed Primitives into a Pure Binary Buffer
    # Header format: 8 bytes for Index, 32 bytes for Prev Hash, 32 bytes for Identity
    binary_header = struct.pack(f">Q32s32s", block_index, prev_bytes, identity_bytes)
    
    # Combine Header + Payload into the final unformatted binary buffer
    raw_binary_buffer = binary_header + payload_bytes
    
    print("\n========================================================")
    print("⚡ COMPUTING PURE BINARY ROOT LAYER: NO TEMPLATES ⚡")
    print("========================================================")
    print(f"[RAW BUFFER SIZE] {len(raw_binary_buffer)} bytes packed in memory.")
    print(f"[BINARY HEX STREAM]\n{raw_binary_buffer.hex()}\n")
    
    # 5. Pass Raw Byte Stream into the Multi-Vector Cascade
    h1 = hashlib.blake2b(raw_binary_buffer).digest()
    h2 = hashlib.sha3_512(h1).digest()
    binary_root_hash = hashlib.sha3_256(h2).hexdigest()
    
    print(f"[BINARY ROOT HASH] 0x{binary_root_hash}")
    print("========================================================")
    return binary_root_hash

if __name__ == "__main__":
    idx = 3  # Targeting the next block space
    payload = "STATE_TRANSITION: BINARY_ROOT_LIQUIDITY_MATRIX_LOCKED" if len(sys.argv) < 2 else sys.argv[1]
    compute_pure_binary_root(idx, payload)
