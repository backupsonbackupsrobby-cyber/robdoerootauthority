// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/721/ERC721.sol";
import "@openzeppelin/contracts/token/721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract SovereignAuthorityNFT is ERC721, ERC721URIStorage, Ownable {
    uint256 private _tokenIds;

    event SovereignTokenMinted(address indexed recipient, uint256 indexed tokenId, string tokenURI);

    constructor() ERC721("RobDoeRootAuthority", "RDRA") Ownable(msg.sender) {}

    function mintSovereignToken(address recipient, string memory uri) 
        public 
        onlyOwner 
        returns (uint256) 
    {
        _tokenIds++;
        uint256 newItemId = _tokenIds;
        
        _safeMint(recipient, newItemId);
        _setTokenURI(newItemId, uri);

        emit SovereignTokenMinted(recipient, newItemId, uri);
        return newItemId;
    }

    function tokenURI(uint256 tokenId)
        public
        view
        override(ERC721, ERC721URIStorage)
        returns (string memory)
    {
        return super.tokenURI(tokenId);
    }

    function supportsInterface(bytes4 interfaceId)
        public
        view
        override(ERC721, ERC721URIStorage)
        returns (bool)
    {
        return super.supportsInterface(interfaceId);
    }
}
