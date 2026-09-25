// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/Strings.sol";

/**
 * @title AtomTruthSovereignGenesis
 * @author RobDoe Pty Ltd | AiAgency101
 * @notice Production-grade 5001 Sovereign Ledger Genesis Contract (5,000 Bundles + 1 Solo Remainder)
 */
contract AtomTruthSovereignGenesis is ERC721, Ownable {
    using Strings for uint256;

    uint256 public constant MAX_SUPPLY = 5001;
    uint256 private _nextTokenId;
    string private _baseTokenURI;
    string public masterRootHash;

    event GenesisMintLocked(address indexed recipient, uint256 startId, uint256 quantity, string rootHash);

    constructor(
        string memory baseURI_,
        string memory initialRootHash
    ) ERC721("AtomTruthSovereign", "ATOM") Ownable(msg.sender) {
        _baseTokenURI = baseURI_;
        masterRootHash = initialRootHash;
        _nextTokenId = 1;
    }

    function _baseURI() internal view override returns (string memory) {
        return _baseTokenURI;
    }

    function setBaseURI(string memory newBaseURI) external onlyOwner {
        _baseTokenURI = newBaseURI;
    }

    function updateMasterRootHash(string memory newRootHash) external onlyOwner {
        masterRootHash = newRootHash;
    }

    function genesisMint(address recipient, uint256 quantity) external onlyOwner {
        require(quantity > 0, "Quantity must be greater than zero");
        require(_nextTokenId + quantity - 1 <= MAX_SUPPLY, "Exceeds max supply of 5001");

        uint256 startId = _nextTokenId;
        for (uint256 i = 0; i < quantity; i++) {
            uint256 tokenId = _nextTokenId++;
            _safeMint(recipient, tokenId);
        }

        emit GenesisMintLocked(recipient, startId, quantity, masterRootHash);
    }

    function tokenURI(uint256 tokenId) public view virtual override returns (string memory) {
        _requireOwned(tokenId);
        string memory baseURI = _baseURI();
        return bytes(baseURI).length > 0 ? string(abi.encodePacked(baseURI, tokenId.toString(), ".json")) : "";
    }
}
