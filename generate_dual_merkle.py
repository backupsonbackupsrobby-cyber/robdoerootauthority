import subprocess
import hashlib

def build_merkle(leaves, algo="sha256"):
    if not leaves:
        return "EMPTY"
    
    def hash_fn(data_bytes):
        if algo == "sha512":
            return hashlib.sha512(data_bytes).hexdigest()
        return hashlib.sha256(data_bytes).hexdigest()

    current_layer = [hash_fn(leaf.encode('utf-8')) for leaf in leaves]
    
    while len(current_layer) > 1:
        next_layer = []
        if len(current_layer) % 2 != 0:
            current_layer.append(current_layer[-1])
        
        for i in range(0, len(current_layer), 2):
            combined = (current_layer[i] + current_layer[i+1]).encode('utf-8')
            next_layer.append(hash_fn(combined))
            
        current_layer = next_layer
        
    return current_layer[0]

# Extract all Git object hashes
rev_result = subprocess.run(["git", "rev-list", "--all", "--objects"], capture_output=True, text=True)
raw_objects = [line.split()[0] for line in rev_result.stdout.strip().split('\n') if line.strip()]

sha256_root = build_merkle(raw_objects, "sha256")
sha512_root = build_merkle(raw_objects, "sha512")

print("\n==================================================================================")
print(f"OBJECT COUNT : {len(raw_objects)} Git Objects Verified")
print(f"SHA-256 ROOT : {sha256_root}")
print(f"SHA-512 ROOT : {sha512_root}")
print("==================================================================================\n")

# Write hex payload to local state dump
with open("merkle_hex_vomit.txt", "w") as f:
    f.write(f"GIT_OBJECTS={len(raw_objects)}\n")
    f.write(f"MERKLE_SHA256={sha256_root}\n")
    f.write(f"MERKLE_SHA512={sha512_root}\n")
