const { Web3 } = require("web3");
require("dotenv").config();

const contractABI = require("../blockchain/build/contracts/AccessControl.json").abi;

const web3 = new Web3(process.env.RPC_URL);
const contract = new web3.eth.Contract(contractABI, process.env.CONTRACT_ADDRESS);

module.exports = { web3, contract };