from flask import Flask, render_template
import subprocess as sp

app = Flask(__name__)

# route decorators
@app.route("/")
def home():
    return render_template("Home.html")

@app.route("/")
def portfolio():
    out = sp.run(["php","portfolio.php"], stdout=sp.PIPE)
    return out.stdout

@app.route("/")
def signup():
    return render_template("SignUpPage.html")

if __name__ == '__main__':
    app.run(debug=True)

app.static_folder = 'static'