// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

/**
 * @title WriteNFD
 * @dev ERC-721 Non-Fungible Domain contract for aiagency101.
 * Hardcoded with NK-SEL v1.0 and native erc721.com domain suffix mapping.
 */
contract WriteNFD is ERC721, Ownable {
    
    error DomainAlreadyExists(string domainName);
    error InvalidDomainSuffix(string domainName);
    error NotAuthorized();

    string public constant NK_SEL_LICENSE = "NK-SEL v1.0: Unauthorized extraction of aiagency101 assets is prohibited. Such is life.";
    string public constant REQUIRED_SUFFIX = ".erc721.com";

    uint256 private _nextTokenId;

    mapping(uint256 => string) private _domainNames;
    mapping(string => bool) private _domainExistsMap;
    mapping(uint256 => string) private _tokenStateProofs;

    event DomainMinted(uint256 indexed tokenId, string domainName, string licenseNotice);
    event StateProofUpdated(uint256 indexed tokenId, string stateProof);

    constructor(address initialOwner) 
        ERC721("WriteNFD", "WNFD") 
        Ownable(initialOwner) 
    {}

    // Enforce native erc721.com suffix verification
    function _endsWith(string memory source, string memory suffix) internal pure returns (bool) {
        bytes memory bSource = bytes(source);
        bytes memory bSuffix = bytes(suffix);
        if (bSource.length < bSuffix.length) {
            return false;
        }
        for (uint i = 0; i < bSuffix.length; i++) {
            if (bSource[bSource.length - bSuffix.length + i] != bSuffix[i]) {
                return false;
            }
        }
        return true;
    }

    function safeMintDomain(address recipient, string memory domainName, string memory stateProof) public onlyOwner returns (uint256) {
        if (!_endsWith(domainName, REQUIRED_SUFFIX)) {
            revert InvalidDomainSuffix(domainName);
        }
        if (_domainExistsMap[domainName]) {
            revert DomainAlreadyExists(domainName);
        }

        uint256 tokenId = ++_nextTokenId;
        
        _domainExistsMap[domainName] = true;
        _domainNames[tokenId] = domainName;
        _tokenStateProofs[tokenId] = stateProof;
        
        _safeMint(recipient, tokenId);
        
        emit DomainMinted(tokenId, domainName, NK_SEL_LICENSE);
        emit StateProofUpdated(tokenId, stateProof);
        return tokenId;
    }

    function getDomainName(uint256 tokenId) public view returns (string memory) {
        _requireOwned(tokenId);
        return _domainNames[tokenId];
    }

    function getStateProof(uint256 tokenId) public view returns (string memory) {
        _requireOwned(tokenId);
        return _tokenStateProofs[tokenId];
    }
}
