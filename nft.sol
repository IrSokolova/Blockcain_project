//Contract based on [https://docs.openzeppelin.com/contracts/3.x/erc721](https://docs.openzeppelin.com/contracts/3.x/erc721)
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract My_NFT{
    // Token name
    string public _name;

    // Token symbol
    string public _symbol;

    mapping(uint256 => address) public _owners;

    mapping(address => uint256) public _balances;

    uint256[] public tokenIDs;

    constructor() payable  {
        _name = "OrangeNFT";
        _symbol = "ONFT";
    }

    function mintNFTs() public returns(bool) {
        uint256 currentID = 1;
        for(uint i = 0; i < 5; i++){
            tokenIDs.push(currentID);

            _owners[currentID] = address(0);
            currentID++;
        }
        return true;
    }

    function buyNFT(uint256 tokenID) public payable returns (bool){
        require(_owners[tokenID] == address(0), "This NFT is already owned");
        require(_balances[msg.sender] >= 1, "You dont have enough coin to buy this NFT");

        //        Reduce the balance of the buyer
        _balances[msg.sender] = _balances[msg.sender] - 1;
        //        Mark this NFT as taken
        _owners[tokenID] = msg.sender;
        return true;
    }

    function sellNFT(uint256 tokenID) public payable returns (bool){
        require(_owners[tokenID] == msg.sender, "You do not own this NFT");

        _balances[msg.sender] = _balances[msg.sender] + 1;
        _owners[tokenID] = address(0);
        return true;
    }

    function viewAvailableNFTs() view external returns (uint256[] memory){
        uint256[] memory availableNFTs = new uint256[](tokenIDs.length);
        uint256 index = 0;
        for (uint i = 0; i < tokenIDs.length; i++){
            if (_owners[tokenIDs[i]] == address(0)){
                availableNFTs[index] = tokenIDs[i];
                index ++;
            }
        }
        return availableNFTs;
    }
}