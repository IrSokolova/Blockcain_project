from flask import Flask, render_template, url_for, request

from init import store

app = Flask(__name__, template_folder='templates')


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/nfts")
def nfts():
    return render_template("nfts.html", nfts=store.nfts)


@app.route("/nft_page")
def nft_page():
    nft_id = request.args.get('nft_id')
    print(nft_id)
    nft = store.find_nft_by_id(int(nft_id))
    return render_template("nft_page.html", nft=nft)


@app.route("/account")
def account():
    username = request.args.get('username')  # todo no such username
    images = [url_for('static', filename=nft.pic_path) for nft in store.users[username].nfts]
    print(images)

    return render_template("user_page.html", images=images)


# api for bot below


@app.route("/registration")
def registration():  # todo addr or uname already exists
    username = request.args.get('username')
    address = request.args.get('address')
    store.registration(address, username)
    print(store.users)
    return "registered"


@app.route("/user_exists")
def user_exists():
    username = request.args.get('username')
    return username_exists(username)


def username_exists(username):
    return str(username in store.users.keys())


def run_front():
    app.run(host="127.0.0.1", port=8081, debug=True)


if __name__ == "__main__":
    run_front()
