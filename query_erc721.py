from web3 import Web3

# Connect to the blockchain RPC endpoint
RPC_URL = "https://eth.llamarpc.com" 
w3 = Web3(Web3.HTTPProvider(RPC_URL))

if not w3.is_connected():
    print("[-] Error: Failed to connect to RPC node.")
    exit()

print("[+] Connected to blockchain RPC successfully!")

# Replace with your target ERC-721 contract address and token ID
CONTRACT_ADDRESS = w3.to_checksum_address("0x0000000000000000000000000000000000000000") 
TOKEN_ID = 1

# Standard ERC-721 ABI for metadata and ownership
FULL_ABI = [
    {
        "constant": True, 
        "inputs": [{"name": "tokenId", "type": "uint256"}], 
        "name": "ownerOf", 
        "outputs": [{"name": "", "type": "address"}], 
        "type": "function"
    },
    {
        "constant": True, 
        "inputs": [], 
        "name": "name", 
        "outputs": [{"name": "", "type": "string"}], 
        "type": "function"
    },
    {
        "constant": True, 
        "inputs": [], 
        "name": "symbol", 
        "outputs": [{"name": "", "type": "string"}], 
        "type": "function"
    },
    {
        "constant": True, 
        "inputs": [{"name": "tokenId", "type": "uint256"}], 
        "name": "tokenURI", 
        "outputs": [{"name": "", "type": "string"}], 
        "type": "function"
    }
]

contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=FULL_ABI)

try:
    name = contract.functions.name().call()
    symbol = contract.functions.symbol().call()
    owner = contract.functions.ownerOf(TOKEN_ID).call()
    uri = contract.functions.tokenURI(TOKEN_ID).call()
    
    print(f"[+] Namespace Collection: {name} ({symbol})")
    print(f"[+] Token ID {TOKEN_ID} Owner: {owner}")
    print(f"[+] Resolution URI / Metadata Pointer: {uri}")
except Exception as e:
    print(f"[-] Execution error or invalid contract interface: {e}")
