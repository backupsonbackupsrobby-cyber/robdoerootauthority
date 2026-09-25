// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "forge-std/Script.sol";
import "../contracts/WriteNFD.sol";

contract DeployAndMint is Script {
    function run() external {
        uint256 deployerPrivateKey = vm.envUint("PRIVATE_KEY");
        address deployer = vm.addr(deployerPrivateKey);

        vm.startBroadcast(deployerPrivateKey);

        // Deploy WriteNFD contract
        WriteNFD nfd = new WriteNFD(deployer);
        
        // Execute Genesis Mint with domain and Merkle root state proof
        string memory domainName = "genesis-1790332647-e09336c4d04a.com";
        string memory stateProof = "0x0c4241e0c5a96ccfc7e952c135a4bd16d8223239e7ababcc62cba82fd0ff4666";
        
        nfd.safeMintDomain(deployer, domainName, stateProof);

        vm.stopBroadcast();
    }
}
