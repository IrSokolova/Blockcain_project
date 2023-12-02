from flask import Flask, render_template, url_for, request

from init import store

app = Flask(__name__, template_folder='templates')


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


@app.route("/registration")
def registration():  # todo addr or uname already exists
    username = request.args.get('username')
    address = request.args.get('address')
    store.registration(address, username)
    print(store.users)
    return "registered"


def run_front():
    app.run(host="127.0.0.1", port=8081, debug=True)


if __name__ == "__main__":
    run_front()
