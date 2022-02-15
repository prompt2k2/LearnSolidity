from solcx import compile_standard, install_solc
import json
from web3 import Web3
import os

install_solc("0.8.11")

with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()

# compile the solidity file

compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"]
                }
            }
        },
    },
    solc_version="0.8.11",
)


with open("deployed_code.json", "w") as file_writer:
    json.dump(compiled_sol, file_writer)

    # get bytecode source
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"][
    "bytecode"
]["object"]

# get abi
abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]

# for connecting to Ganache
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
chain_id = 5777
wallet_address = "0x90F8bf6A479f320ead074411a4B0e7944Ea8c9C1"
wallet_key = "0x4f3edf983ac636a65a842ce7c78d9aa706d3b113bce9c46f30d7d21715b23b1d"#os.environ.get("ETH_PRIVATE_KEY")

# connect contract to ganache

SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)

# Get latest transaction from
nonce = w3.eth.getTransactionCount(
    wallet_address
)  # gets the number of transaction in that address.
# print(nonce)
transaction = SimpleStorage.constructor().buildTransaction(
    {
        "gasPrice": w3.eth.gas_price,
        "from": wallet_address,
        "nonce": nonce,
    }
)
signed_transaction = w3.eth.account.sign_transaction(
    transaction, private_key=wallet_key
)

print("Deploying Contract...")
## send the signed transaction
tx_hash = w3.eth.send_raw_transaction(signed_transaction.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
############################################################################
# Working with the created contract requires the contract Address and the ABI
print("...Contract Deployed!")
simple_storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)


# Using .call() because we are not trying to make a state change, else .transact()
print(simple_storage.functions.retrieve().call())  
print("...Updating Contract...Please wait...")
store_transaction = simple_storage.functions.store(55).buildTransaction(
    {"gasPrice":w3.eth.gas_price,"from": wallet_address, "nonce": nonce + 1}
)  # Nonce plus 1 because the nonce had been used once to build the transaction


#state change happens here
signed_store_tx = w3.eth.account.sign_transaction(
    store_transaction,  private_key=wallet_key
)

send_store_tx = w3.eth.send_raw_transaction(signed_store_tx.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(send_store_tx)
print("...Contract Updated!!!!")

print(simple_storage.functions.retrieve().call())  