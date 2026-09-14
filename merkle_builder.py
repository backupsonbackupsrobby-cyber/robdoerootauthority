import hashlib

def sha256(data: str) -> str:
    return hashlib.sha256(data.encode('utf-8')).hexdigest()

# Extracted leaves from converged Kuramoto execution
leaves = [
    "9fef61eb4eea75a8",
    "06262341d56358c0",
    "5011bb51672b5f3d",
    "fdb87c59dc5ead1c",
    "8d59da4828624baf"
]

print("--- SHA-256 MERKLE TREE CONSTRUCTION ---")
for i, leaf in enumerate(leaves):
    print(f"Leaf [{i}]: {leaf}")

# Layer 1: Pairwise Hashing
parent_0 = sha256(leaves[0] + leaves[1])
parent_1 = sha256(leaves[2] + leaves[3])
parent_2 = sha256(leaves[4] + leaves[4])  # Duplicate odd leaf

print(f"\nNode [0+1]: {parent_0[:16]}...")
print(f"Node [2+3]: {parent_1[:16]}...")
print(f"Node [4+4]: {parent_2[:16]}...")

# Layer 2 & Merkle Root
root_left = sha256(parent_0 + parent_1)
merkle_root = sha256(root_left + parent_2)

print(f"\n========================================")
print(f"FINAL MERKLE ROOT: {merkle_root}")
print(f"========================================")
