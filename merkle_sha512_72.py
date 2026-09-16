import hashlib


def sha512_iterative(data: bytes, iterations: int = 72) -> bytes:
  """Applies SHA-512 iteratively N times (72 rounds)."""
  current = data
  for _ in range(iterations):
    current = hashlib.sha512(current).digest()
  return current


def hash_node(left: bytes, right: bytes = b'') -> bytes:
  """Computes a standard SHA-512 hash for a parent tree node."""
  return hashlib.sha512(left + right).digest()


def compute_merkle_root_with_leaf_transforms(leaves: list[str]) -> str:
  """Transforms every leaf using sha512x72, then builds the Merkle tree root."""
  if not leaves:
    return hashlib.sha512(b'').digest().hex()

  # Step 1: Apply sha512x72 to EVERY individual leaf node
  transformed_leaves = []
  for leaf in leaves:
    leaf_bytes = leaf.encode('utf-8')
    sealed_leaf = sha512_iterative(leaf_bytes, 72)
    transformed_leaves.append(sealed_leaf)

  # Step 2: Build the binary Merkle tree from the transformed leaves
  current_level = transformed_leaves
  while len(current_level) > 1:
    next_level = []
    for i in range(0, len(current_level), 2):
      left = current_level[i]
      # If odd number of nodes, duplicate the last one
      right = current_level[i + 1] if i + 1 < len(current_level) else left
      next_level.append(hash_node(left, right))
    current_level = next_level

  # Return final Merkle root hex
  return current_level[0].hex()


if __name__ == '__main__':
  # Active state leaves for your workspace
  sample_leaves = ['GENESIS_NODE_A', 'GENESIS_NODE_B', 'GENESIS_NODE_C']

  root_hex = compute_merkle_root_with_leaf_transforms(sample_leaves)
  print(f'Final Merkle Root Hash (sha512x72 leaves): {root_hex}')
