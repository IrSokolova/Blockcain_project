from back.nft import Nft
from back.store import Store

store = Store([Nft(1, '', 1, 'img.png'),
               Nft(2, '', 2, 'img_1.png'),
               Nft(3, '', 3, 'img_2.png'),
               Nft(4, '', 4, 'img_3.png'),
               Nft(5, '', 5, 'img_4.png'),
               ])
# dict = {"orange1": }
store.registration("", "u1")

