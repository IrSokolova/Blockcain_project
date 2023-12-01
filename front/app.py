from flask import Flask, render_template, url_for, request

from back.nft import Nft
from back.store import Store

app = Flask(__name__, template_folder='templates')
store = Store([Nft(0, '', 0, 'img.png'),
               Nft(0, '', 0, 'img_1.png'),
               Nft(0, '', 0, 'img_2.png')])
# dict = {"orange1": }
store.registration("", "u1")
store.users["u1"].add_nft(Nft(0, '', 0, 'img_3.png'))
store.users["u1"].add_nft(Nft(0, '', 0, 'img_4.png'))


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/nfts")
def nfts():
    images = [url_for('static', filename=nft.pic_url) for nft in store.nfts]
    return render_template("nfts.html", images=images)


@app.route("/account")
def account():
    username = request.args.get('username')  # todo no such username
    images = [url_for('static', filename=nft.pic_url) for nft in store.users[username].nfts]
    print(images)

    return render_template("user_page.html", images=images)
    # return render_template("user_page.html", image1=url_for('static', filename='img.png'))
    # return render_template("user_page.html", title="Hello World")


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
