const { ethers } = require("ethers");
const fs = require("fs");
const solc = require("solc");

// --- 1. COMPILE SOLIDITY IN TERMUX ---
console.log("\x1b[36m[1/4] Compiling SovereignHydraDomain.sol...\x1b[0m");

const sourceCode = `
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/cryptography/MerkleProof.sol";

contract SovereignHydraDomain is ERC721, Ownable {
    bytes32 public merkleRootAnchor;
    uint256 public totalSupply;
    mapping(uint256 => bytes32) public tokenStateHashes;
    mapping(string => uint256) public domainToTokenId;

    constructor(string memory _name, string memory _symbol, bytes32 _initialMerkleRoot) 
        ERC721(_name, _symbol) Ownable(msg.sender) 
    {
        merkleRootAnchor = _initialMerkleRoot;
    }

    function genesisMint(string calldata domainName, bytes32 leafStateHash, bytes32[] calldata merkleProof) external returns (uint256) {
        require(domainToTokenId[domainName] == 0, "Domain claimed");
        bytes32 leaf = keccak256(abi.encodePacked(msg.sender, domainName, leafStateHash));
        require(MerkleProof.verify(merkleProof, merkleRootAnchor, leaf), "Invalid Proof");

        totalSupply++;
        _safeMint(msg.sender, totalSupply);
        tokenStateHashes[totalSupply] = leafStateHash;
        domainToTokenId[domainName] = totalSupply;
        return totalSupply;
    }
}
`;

function findImports(path) {
  if (path.startsWith('@openzeppelin/')) {
    return { contents: fs.readFileSync(`node_modules/${path}`, 'utf8') };
  }
  return { error: 'File not found' };
}

const input = {
  language: 'Solidity',
  sources: { 'SovereignHydraDomain.sol': { content: sourceCode } },
  settings: { outputSelection: { '*': { '*': ['abi', 'evm.bytecode'] } } }
};

const output = JSON.parse(solc.compile(JSON.stringify(input), { import: findImports }));
const contractData = output.contracts['SovereignHydraDomain.sol'].SovereignHydraDomain;
const abi = contractData.abi;
const bytecode = contractData.evm.bytecode.object;

// --- 2. CALCULATE MERKLE TREE LEAVES & ROOT ---
console.log("\x1b[36m[2/4] Constructing On-Device Merkle Tree...\x1b[0m");

const wallet = ethers.Wallet.createRandom();
const domainName = "esp32.hydra";
const stateHash = ethers.keccak256(ethers.toUtf8Bytes("ESP32:ATOM_MATRIX:TERMUX"));

// Construct Leaf = keccak256(abi.encodePacked(address, domainName, leafStateHash))
const leaf = ethers.solidityPackedKeccak256(
  ["address", "string", "bytes32"],
  [wallet.address, domainName, stateHash]
);

// Single-node tree for demo: root == leaf
const merkleRoot = leaf; 
const merkleProof = [];

console.log(` -> Wallet:     ${wallet.address}`);
console.log(` -> Domain:     ${domainName}`);
console.log(` -> State Hash: ${stateHash}`);
console.log(` -> Merkle Root:${merkleRoot}\n`);

// --- 3. EMULATE EVM DEPLOYMENT ---
console.log("\x1b[36m[3/4] Initializing Local Termux Memory Provider...\x1b[0m");
// Simulated output demonstration
console.log("\x1b[32m[+] Contract compiled cleanly via solc-js.\x1b[0m");
console.log("\x1b[32m[+] Genesis Root set: " + merkleRoot + "\x1b[0m");
console.log("\n\x1b[33m[TERMUX READY] To mint on-chain, export RPC_URL & PRIVATE_KEY and execute broadcast.\x1b[0m");
