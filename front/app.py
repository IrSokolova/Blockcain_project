from flask import Flask, render_template

app = Flask(__name__, template_folder='templates')


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/nfts")
def nfts():
    return render_template("nfts.html")


@app.route("/account")
def account():
    return render_template("user_page.html")
    # return render_template("user_page.html", title="Hello World")


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
