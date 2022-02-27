from flask import Flask, render_template
from flask_breadcrumbs import Breadcrumbs, register_breadcrumb 

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/")
def signup():
    return render_template("SignUpPage.html")

app.static_folder = 'static'