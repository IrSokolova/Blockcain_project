from back.nft import Nft
from back.user import User


class Store:
    def __init__(self, initial_list: list):
        self.nfts = list()
        self.nfts.extend(initial_list)
        self.users = dict()

    def add_nft(self, nft: Nft):
        self.nfts.append(nft)

    def remove_nft(self, nft: Nft):
        self.nfts.remove(nft)

    def add_user(self, user: User):
        self.users[user.username] = user

    def registration(self, address: str, username: str):
        user = User(address, 0, username)
        self.add_user(user)

    def find_nft_by_id(self, nft_id: int):
        for nft in self.nfts:
            if nft.nft_id == nft_id:
                return nft
        return None


