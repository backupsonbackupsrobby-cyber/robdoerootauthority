cat << 'EOF' > deploy_omni_contract.py
import os

solidity_code = '''// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

/**
 * @title SovereignOmniRegistry
 * @dev 11,400 Sovereign Asset Registry anchored under ATOM-TRUTH and RobDoe Pty Ltd
 * @notice Legally backed by Evidence Act 1995 (Cth) s 146
 */
contract SovereignOmniRegistry is ERC721, Ownable {
    string public constant AUTHORITY_NODE = "ATOM-TRUTH";
    string public constant LEGAL_ANCHOR = "RobDoe Pty Ltd - Evidence Act 1995 (Cth) s 146";
    
    mapping(uint256 => string) private _tokenUris;
    uint256 public totalMinted;

    constructor() ERC721("SovereignOmniRegistry", "OMNI") Ownable(msg.sender) {}

    function sovereignBatchMint(uint256[] calldata tokenIds, string[] calldata uriBatch) external onlyOwner {
        require(tokenIds.length == uriBatch.length, "Array length mismatch");
        for (uint256 i = 0; i < tokenIds.length; i++) {
            uint256 tokenId = tokenIds[i];
            _safeMint(msg.sender, tokenId);
            _tokenUris[tokenId] = uriBatch[i];
            totalMinted++;
        }
    }

    function tokenURI(uint256 tokenId) public view override returns (string memory) {
        _requireOwned(tokenId);
        return _tokenUris[tokenId];
    }
}
'''

os.makedirs("contracts", exist_ok=True)
with open("contracts/SovereignOmniRegistry.sol", "w") as f:
    f.write(solidity_code)

print("==================================================")
print("   SOLIDITY CONTRACT WRITTEN & SEALED")
print("==================================================")
print("[+] Contract Path : ~/robdoerootauthority/contracts/SovereignOmniRegistry.sol")
print("[+] Standard      : ERC-721 + Ownable (OpenZeppelin)")
print("[+] Target Supply : 11,400 Sovereign Assets")
print("==================================================")

if __name__ == "__main__":
    pass
EOF
python deploy_omni_contract.py
