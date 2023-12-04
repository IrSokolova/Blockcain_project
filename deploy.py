import os

from web3 import Web3
from solcx import compile_standard, install_solc
import json


with open("../nft.sol", "r") as file:
    smart_contract_nft = file.read()

install_solc("0.8.0")

# Solidity source code
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"nft.sol": {"content": smart_contract_nft}},
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]
                }
            }
        }
    },
    solc_version="0.8.0",
)

with open("compiled_code.json","w") as file:
    json.dump(compiled_sol,file)

# get abi
abi = compiled_sol["contracts"]["nft.sol"]["NFT"]["abi"]

# bytecode
bytecode = compiled_sol["contracts"]["nft.sol"]["NFT"]["evm"]["bytecode"]["object"]


w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))
chain_id = 5777
my_address = "0x30afafbBedEfBF93888B7362FF49B91c8bCD546F"
# my_address = "0x5BcE8A16e63fe61c4205581412cD93824871fd47"
private_key = os.getenv("PRIVATE_KEY")

SmartContract = w3.eth.contract(abi=abi, bytecode=bytecode)

nonce = w3.eth.get_transaction_count(w3.eth.coinbase)

transaction = SmartContract.constructor().build_transaction({
    "chainId": w3.eth.chain_id,
    "gasPrice": w3.eth.gas_price,
    "from": my_address,
    "nonce": nonce,
})

print(transaction)

# Sign the transaction
signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)

print("Deploying Contract!")
# Sent it
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)

# Wait for the transaction to be mined, and get the transaction receipt
print("Waiting for Transaction to finish...")

tx_receipt=w3.eth.wait_for_transaction_receipt(tx_hash)
print(f"Done! Contract Deployed to {tx_receipt.contractAddress}")

print(SmartContract.all_functions())

smart_contract_demo = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)
functions = smart_contract_demo.functions
# print(functions.mintNFTs().call())
# print(functions._owners(1).call())
# print(functions.buyNFT(1).call())
