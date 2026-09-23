import requests
import json
from Crypto.Hash import keccak

def get_namehash(domain: str) -> bytes:
    node = b'\x00' * 32
    for label in reversed(domain.lower().strip().split('.')):
        k = keccak.new(digest_bits=256)
        k.update(label.encode('utf-8'))
        label_hash = k.digest()
        k2 = keccak.new(digest_bits=256)
        k2.update(node + label_hash)
        node = k2.digest()
    return node

domain_name = "robdoe.crypto"
node_bytes = get_namehash(domain_name)
token_id_int = int.from_bytes(node_bytes, byteorder='big')

PROXY_READER = "0xa9a53c106473518171351c0f24e5d23326f58278"
token_id_hex = hex(token_id_int)[2:].zfill(64)
calldata = "0x6352211e" + token_id_hex

payload = {
    "jsonrpc": "2.0",
    "method": "eth_call",
    "params": [{
        "to": PROXY_READER,
        "data": calldata
    }, "latest"],
    "id": 1
}

# Reliable public Polygon RPC
rpc_url = "https://1rpc.io/matic"
response = requests.post(rpc_url, json=payload)
result = response.json()

print(f"Domain: {domain_name}")
print(f"TokenID (Dec): {token_id_int}")

if "result" in result and result["result"] != "0x":
    owner_address = "0x" + result["result"][-40:]
    print(f"[VERIFIED] On-Chain Owner Address: {owner_address}")
else:
    print(f"[ERROR] Query failed: {result}")
