// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts/utils/Counters.sol";


contract Randomizer
{
    // Initializing the state variable
    uint randNonce = 0;

    // Defining a function to generate
    // a random number
    function randMod(uint _modulus) external returns(uint)
    {
        // increase nonce
        randNonce++;
        return uint(keccak256(abi.encodePacked(block.timestamp,msg.sender,randNonce))) % _modulus;
    }
}


contract BasicNFT is ERC721URIStorage {
    using Counters for Counters.Counter;
    Counters.Counter private _tokenIds;
    mapping (uint256 => uint256) pricesOfNFTs;
    mapping (address => uint256) balances;
    mapping (uint256 => address) ownedNFTs;
    Randomizer randomizer;

    constructor() ERC721("BasicNFT", "BNFT") {}

    function createNFTs(uint NFTsCount) {
        for(uint i=0; i<NFTsCount; i++){
            _tokenIds.increment();
            uint256 newItemId = _tokenIds.current();

            pricesOfNFTs[newItemId] = randomizer.randMod(10);
            ownedNFTs[newItemId] = address(0);
        }
    }

    function buy(uint256 tokenID) public {
        require(ownedNFTs[tokenID] != address(0), "This NFT is already owned");
        require(balances[msg.sender] >= pricesOfNFTs[tokenID], "You dont have enough coin to buy this NFT");

//        Reduce the balance of the buyer
        balances[msg.sender] = balances[msg.sender] - pricesOfNFTs[tokenID];
//        Mark this NFT as taken
        ownedNFTs[tokenID] = msg.sender;
    }

    function sell(uint tokenID) public {
        require(ownedNFTs[tokenID] == msg.sender, "You aren't the owner of this NFT");

//        Increase the balance of the seller
        balances[msg.sender] = balances[msg.sender] + pricesOfNFTs[tokenID];
//        Change address of NFT
        ownedNFTs[tokenID] = address(0);
    }
}