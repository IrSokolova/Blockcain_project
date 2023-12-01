from back.nft import Nft


class User:
    def __init__(self, address: str, balance: int, username: str):
        self.nfts = list()
        self.address = address
        self.balance = balance
        self.username = username

    def add_nft(self, nft: Nft):
        self.nfts.append(nft)

    def remove_nft(self, nft: Nft):
        self.nfts.remove(nft)



