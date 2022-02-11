// SPDX-License-Identifier: MIT

pragma solidity 0.8.11;

import "./SimpleStorage.sol"; 

contract StorageFactory is SimpleStorage {//the "is" statement allows StorageFactory to inherit the functions and variables of SimpleStorage
    
    SimpleStorage[] public ssArray;
    
    function createSimpleStorageContract() public { //create or interact with a contract from another contract
        SimpleStorage sStorage = new SimpleStorage();
        ssArray.push(sStorage);
    }
    
    function sfStore(uint256 _simpleStorageIndex, uint256 _simpleStorageNumber) public {
        // Address 
        // ABI 
        return SimpleStorage(address(ssArray[_simpleStorageIndex])).store(_simpleStorageNumber);
       //this line has an explicit cast to the address type and initializes a new SimpleStorage object from the address
        

        //this line simply gets the SimpleStorage object at the index _simpleStorageIndex in the array simpleStorageArray
        //simpleStorageArray[_simpleStorageIndex].store(_simpleStorageNumber);
    }
    
    function sfGet(uint256 _simpleStorageIndex) public view returns (uint256) {
        return SimpleStorage(address(ssArray[_simpleStorageIndex])).retrieve();

    }
  
        //this line has an explicit cast to the address type and initializes a new SimpleStorage object from the address 
        //return SimpleStorage(address(simpleStorageArray[_simpleStorageIndex])).retrieve(); 
} 