from deploy import w3, private_key, my_address


class Contract:
    def __init__(self, functions):
        self.functions = functions
        self.functions.mintNFTs().call()

    def buy_nft(self, nft_id: int, address: str):
        self.functions.buyNFT(nft_id, address).call()
        nonce = w3.eth.get_transaction_count(w3.eth.coinbase)
        trans = self.functions.buyNFT(nft_id, address).build_transaction({
            "chainId": w3.eth.chain_id,
            "gasPrice": w3.eth.gas_price,
            "from": my_address,
            "nonce": nonce,
        })
        signed_txn = w3.eth.account.sign_transaction(trans, private_key=private_key)
        tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        w3.eth.wait_for_transaction_receipt(tx_hash)

    def sell_nft(self, nft_id: int, address: str):
        self.functions.sellNFT(nft_id, address).call()
        nonce = w3.eth.get_transaction_count(w3.eth.coinbase)
        trans = self.functions.sellNFT(nft_id, address).build_transaction({
            "chainId": w3.eth.chain_id,
            "gasPrice": w3.eth.gas_price,
            "from": my_address,
            "nonce": nonce,
        })
        signed_txn = w3.eth.account.sign_transaction(trans, private_key=private_key)
        tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        w3.eth.wait_for_transaction_receipt(tx_hash)
