from back.nft import Nft
from back.store import Store

store = Store([Nft(0, '', 0, 'img.png'),
               Nft(0, '', 0, 'img_1.png'),
               Nft(0, '', 0, 'img_2.png')])
# dict = {"orange1": }
store.registration("", "u1")
store.users["u1"].add_nft(Nft(0, '', 0, 'img_3.png'))
store.users["u1"].add_nft(Nft(0, '', 0, 'img_4.png'))

