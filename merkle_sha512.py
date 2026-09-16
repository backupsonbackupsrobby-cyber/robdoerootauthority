import hashlib


def sha512_iterative(data: bytes, iterations: int = 13000) -> bytes:
  """Applies SHA-512 iteratively N times."""
  current = data
  for _ in range(iterations):
    current = hashlib.sha512(current).digest()
  return current


def hash_node(left: bytes, right: bytes = b'') -> bytes:
  """Computes a SHA-512 hash for a tree node."""
  return hashlib.sha512(left + right).digest()


def compute_merkle_root(leaves: list[bytes]) -> bytes:
  """Builds a binary Merkle tree and returns the root hash."""
  if not leaves:
    return hashlib.sha512(b'').digest()

  current_level = [hash_node(leaf) for leaf in leaves]

  while len(current_level) > 1:
    next_level = []
    for i in range(0, len(current_level), 2):
      left = current_level[i]
      # If odd number of nodes, duplicate the last one
      right = current_level[i + 1] if i + 1 < len(current_level) else left
      next_level.append(hash_node(left, right))
    current_level = next_level

  return current_level[0]


def generate_sovereign_root(leaves: list[str]) -> str:
  # Convert string leaves to bytes
  byte_leaves = [leaf.encode('utf-8') for leaf in leaves]

  # Step 1: Compute standard Merkle Root
  merkle_root = compute_merkle_root(byte_leaves)

  # Step 2: Apply sha512x13000 transformation
  final_hash_bytes = sha512_iterative(merkle_root, 13000)

  # Return hex representation
  return final_hash_bytes.hex()


if __name__ == '__main__':
  # Example dataset representing your state matrix or blocks
  sample_leaves = ['GENESIS_NODE_A', 'GENESIS_NODE_B', 'GENESIS_NODE_C']

  root_hex = generate_sovereign_root(sample_leaves)
  print(f'Final Root Hash (sha512x13000): {root_hex}')
