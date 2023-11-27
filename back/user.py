from back.nft import Nft


class User:
    def __init__(self, address: str, balance: int):
        self.nft = list()
        self.address = address
        self.balance = balance

    def add_nft(self, nft: Nft):
        self.nft.append(nft)


