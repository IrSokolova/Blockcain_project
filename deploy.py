import os

from web3 import Web3
from solcx import compile_standard, install_solc
import json


with open("./nft.sol", "r") as file:
    smart_contract_nft = file.read()

install_solc("0.8.20")

# Solidity source code
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"nft.sol" : { "content" : smart_contract_nft }},
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi","metadata","evm.bytecode","evm.sourceMap"]
                }
            }
        }
    },
    solc_version="0.8.20",
)

with open("compiled_code.json","w") as file:
    json.dump(compiled_sol,file)

# get abi
abi = compiled_sol["contracts"]["nft.sol"]["My_NFT"]["abi"]

# bytecode
bytecode = compiled_sol["contracts"]["nft.sol"]["My_NFT"]["evm"]["bytecode"]["object"]


w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))
chain_id = 5777
my_address = "0x30afafbBedEfBF93888B7362FF49B91c8bCD546F"
private_key = os.getenv("PRIVATE_KEY")

SmartContract = w3.eth.contract(abi=abi, bytecode=bytecode)

nonce = w3.eth.getTransactionCount(my_address)

transaction = SmartContract.constructor()

print(SmartContract.all_functions())
