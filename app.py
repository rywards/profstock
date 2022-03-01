from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/")
def home():
    return render_template("Home.html")

@app.route("/")
def signup():
    return render_template("SignUpPage.html")

app.static_folder = 'static'