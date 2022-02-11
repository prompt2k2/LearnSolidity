//SPDX-License-Identifier:OpenSSL;

pragma solidity 0.8.0;

contract SimpleStorage{
    uint256  favoriteNumber; //initialises the variable to zero!

    struct People{
        uint256 favoriteNumber;
        string name;
    }

    People public person = People({favoriteNumber:2, name:"James"});

    function store(uint256 _favNum) public {
        favoriteNumber = _favNum;
    }
    //view and pure function
    //view reads off the blockchain without making transactions

    function retrieve() public view returns(uint256){
        return favoriteNumber;
    }
}