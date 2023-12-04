class Contract:
    def __init__(self, functions):
        self.functions = functions
        self.functions.mintNFTs().call()

    def buy_nft(self, nft_id: int):
        self.functions.buyNFT(nft_id).call()

    def sell_nft(self, nft_id: int):
        self.functions.sellNFT(nft_id).call()

