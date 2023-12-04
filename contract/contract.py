from deploy import functions


class Contract:
    def __int__(self):
        self.functions = functions
        functions.mintNFTs().call()

    def buy_nft(self, nft_id):
        self.functions.buyNFT(nft_id).call()

    def sell_nft(self, nft_id):
        self.functions.sellNFT(nft_id).call()

