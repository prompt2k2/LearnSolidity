//SPDX-License-Identifier: MIT
pragma solidity >=0.7.0;


//import "./SimpleStorage.sol";
//import "./StorageFactory.sol";
//import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol/";
//import "https://github.com/smartcontractkit/chainlink/blob/develop/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";
import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol"; //from https://docs.chain.link/docs/get-the-latest-price/
//import "@chainlink/contracts/src/v0.8/vendor/SafeMathChainlink.sol";
import "@OpenZeppelin/contracts/utils/math/SafeMath.sol";


contract FundMe {
    using SafeMath for uint256; //use Safemath for all variables with uint256

    mapping(address => uint256) public addressToAmountFunded;
    address[] public funders;
    address public owner;

    constructor() {
        owner = msg.sender; //makes the address that deploys the contract the owner of the contract.
        } 

    function fund() public payable {
        uint256 minUSD = 50 * 10 ** 18; //Minimum value transferable is 50USD. Raised here to power of 18 for Wei conversion.
        require(getConversionRate(msg.value)>= minUSD, "The amount is not sufficient"); //ensures the recieved amount is not less than 50USD
        addressToAmountFunded[msg.sender] += msg.value; //Sender and the amount they sent.
        funders.push(msg.sender);

    }

    function getVersion() public view returns (uint256) {
        
        AggregatorV3Interface priceFeed = AggregatorV3Interface(0x8A753747A1Fa494EC906cE90E9f37563A8AF630e) ;
        return priceFeed.version();
    }

    function getPrice() public view returns (uint256) {
        AggregatorV3Interface priceFeed = AggregatorV3Interface(0x8A753747A1Fa494EC906cE90E9f37563A8AF630e);
        (,int256 answer,,,) = priceFeed.latestRoundData();
        return uint256(answer * 10000000000);
    }

    function getPriceIR() public view returns (uint256) {
        AggregatorV3Interface priceFeed = AggregatorV3Interface(0x8A753747A1Fa494EC906cE90E9f37563A8AF630e);
        (,,,,uint80 answeredInRound) = priceFeed.latestRoundData();
        return uint80(answeredInRound);
    }
    //convert ethereum sent to usd
    function getConversionRate(uint256 ethAmount) public view returns (uint256){ //ethAmount is the amount in Ether send.
        uint256 ethPrice = getPrice();
        uint256 ethAmountInUSD = (ethPrice * ethAmount) / 1000000000000000000;
        return ethAmountInUSD; //returns the current value of Ethereum in USD
    }

    modifier onlyOwner {
        require(msg.sender ==owner);
        _; //if the require statement is met, it will perform the subequent code.
    }

    function withdraw() payable onlyOwner public { //onlyOwner is calling the modifier. Not required if require keyword is used inline.
        //only the contract winner can withdraw
        //require(msg.sender == owner); //ensure only the owner can call the withdraw function.
        payable(msg.sender).transfer(address(this).balance);
        for (uint256 funderIndex=0; funderIndex<funders.length; funderIndex++){
            address funder = funders[funderIndex];
            addressToAmountFunded[funder]=0;
        }
        funders = new address[](0);
    }
}

