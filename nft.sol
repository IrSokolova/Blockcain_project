//Contract based on [https://docs.openzeppelin.com/contracts/3.x/erc721](https://docs.openzeppelin.com/contracts/3.x/erc721)
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract NFT{
    // Token name
    string private _name;

    // Token symbol
    string private _symbol;

    uint256[] public tokenIDs;

    address public my_address;

    mapping(uint256 => address) private _owners;

    mapping(address => uint256) private _balances;

    mapping(uint256 => address) private _tokenApprovals;

    constructor() {
        _name = "OrangeNFT";
        _symbol = "ONFT";
        my_address = msg.sender;
    }


    function balanceOf(address owner) public view returns (uint256){
        require(owner == address(0), "Null address");
        return _balances[owner];
    }

    function ownerOf(uint256 tokenId) public view virtual returns (address) {
        return _owners[tokenId];
    }

     function _update(address to, uint256 tokenId) internal virtual returns (address) {
        address from = ownerOf(tokenId);

        // Execute the update
        if (from != address(0)) {

            _balances[from] -= 1;
        }

        if (to != address(0)) {
            _balances[to] += 1;
        }

        _owners[tokenId] = to;

        return from;
    }

    function transferFrom(address from, address to, uint256 tokenId) public virtual {
        require(to == address(0), "Null address");
        address previousOwner = _update(to, tokenId);
        require(previousOwner == from);

    }

     function mintNFTs() public {
        uint256 currentID = 1;
        for(uint i = 0; i < 5; i++){
            tokenIDs.push(currentID);

            _owners[currentID] = my_address;
            currentID++;
        }
    }

    function buyNFT(uint256 tokenID, address addr) public payable returns (bool){
        require(_owners[tokenID] == my_address, "This NFT is already owned");
        require(_balances[addr] >= 1, "You dont have enough coin to buy this NFT");

        transferFrom(my_address, addr, tokenID);

        return true;
    }

    function sellNFT(uint256 tokenID, address addr) public payable returns (bool){
        require(_owners[tokenID] == addr, "You do not own this NFT");

        transferFrom(addr, my_address, tokenID);
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