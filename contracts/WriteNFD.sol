// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

/**
 * @title WriteNFD
 * @dev ERC-721 implementation for Non-Fungible Domains supporting full .com suffix tracking.
 */
contract WriteNFD is ERC721, Ownable {
    
    // Custom errors for gas efficiency
    error DomainAlreadyExists(string domainName);
    error NotAuthorized();

    // Counter for tracking token generation
    uint256 private _nextTokenId;

    // Mapping from tokenId to stored domain string (e.g., "telegram.com")
    mapping(uint256 => string) private _domainNames;

    // Mapping from domain name string to existence boolean (prevents duplicate .com entries)
    mapping(string => bool) private _domainExistsMap;

    // Mapping from tokenId to stored state proof / metadata hash
    mapping(uint256 => string) private _tokenStateProofs;

    event DomainMinted(uint256 indexed tokenId, string domainName);
    event StateProofUpdated(uint256 indexed tokenId, string stateProof);

    constructor(address initialOwner) 
        ERC721("WriteNFD", "WNFD") 
        Ownable(initialOwner) 
    {}

    /**
     * @dev Mint a new NFToken domain (including .com) with uniqueness enforcement.
     */
    function safeMintDomain(address recipient, string memory domainName, string memory stateProof) public onlyOwner returns (uint256) {
        if (_domainExistsMap[domainName]) {
            revert DomainAlreadyExists(domainName);
        }

        uint256 tokenId = ++_nextTokenId;
        
        _domainExistsMap[domainName] = true;
        _domainNames[tokenId] = domainName;
        _tokenStateProofs[tokenId] = stateProof;
        
        _safeMint(recipient, tokenId);
        
        emit DomainMinted(tokenId, domainName);
        emit StateProofUpdated(tokenId, stateProof);
        return tokenId;
    }

    /**
     * @dev Update the state proof associated with a specific domain token.
     */
    function updateStateProof(uint256 tokenId, string memory newStateProof) public {
        if (ownerOf(tokenId) != msg.sender && owner() != msg.sender) {
            revert NotAuthorized();
        }
        
        _tokenStateProofs[tokenId] = newStateProof;
        emit StateProofUpdated(tokenId, newStateProof);
    }

    /**
     * @dev Retrieve the fully qualified domain name (e.g., telegram.com) for a given token ID.
     */
    function getDomainName(uint256 tokenId) public view returns (string memory) {
        _requireOwned(tokenId);
        return _domainNames[tokenId];
    }

    /**
     * @dev Retrieve the state proof payload for a given token ID.
     */
    function getStateProof(uint256 tokenId) public view returns (string memory) {
        _requireOwned(tokenId);
        return _tokenStateProofs[tokenId];
    }
}
