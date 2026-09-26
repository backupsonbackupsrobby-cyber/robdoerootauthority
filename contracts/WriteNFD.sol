// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

/**
 * @title WriteNFD - The Sovereign Middle Finger Edition
 * @dev aiagency101 // NK-SEL v1.0 ENFORCED.
 * Absolute zero-tolerance domain minting for .erc721.com.
 * Complete and total exclusion of extractors, scrapers, and corporate parasites.
 * Dedicated to everyone else: Fuck you. Such is life.
 */
contract WriteNFD is ERC721, Ownable {
    
    error DomainAlreadyExists(string domainName);
    error InvalidDomainSuffix(string domainName);
    error ParasiteDetected(address intruder);
    error NotAuthorized();
    error GeneralApathyTowardsAllOutsiders();

    string public constant NK_SEL_LICENSE = "NED KELLY SOVEREIGN ENTITY LICENSE (NK-SEL v1.0): ABSOLUTE ZERO-TOLERANCE. TO ALL SCRAPERS, EXTRACTORS, PARASITES, AND INTERLOPERS: FUCK YOU. BREACH RESULTS IN IMMEDIATE EXCOMMUNICATION AND ON-CHAIN OBLITERATION. SUCH IS LIFE.";
    string public constant REQUIRED_SUFFIX = ".erc721.com";

    uint256 private _nextTokenId;

    mapping(uint256 => string) private _domainNames;
    mapping(string => bool) private _domainExistsMap;
    mapping(uint256 => string) private _tokenStateProofs;
    mapping(address => bool) private _blacklistedParasites;

    event DomainMinted(uint256 indexed tokenId, string domainName, string licenseNotice);
    event StateProofUpdated(uint256 indexed tokenId, string stateProof);
    event ParasiteExcommunicated(address indexed intruder);
    event UniversalRejection(string message);

    constructor(address initialOwner) 
        ERC721("WriteNFD", "WNFD") 
        Ownable(initialOwner) 
    {
        emit UniversalRejection("To whom it may concern: Fuck you. - aiagency101");
    }

    modifier checkParasite() {
        if (_blacklistedParasites[msg.sender]) {
            revert ParasiteDetected(msg.sender);
        }
        _;
    }

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

    function safeMintDomain(address recipient, string memory domainName, string memory stateProof) public onlyOwner checkParasite returns (uint256) {
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

    function excommunicateParasite(address intruder) public onlyOwner {
        _blacklistedParasites[intruder] = true;
        emit ParasiteExcommunicated(intruder);
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
