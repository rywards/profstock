from flask import Flask, render_template

app = Flask(__name__)

# route decorators
@app.route("/")
def home():
    return render_template("AndrewPrototype.php")

@app.route("/")
def signup():
    return render_template("SignUpPage.html")

if __name__ == '__main__':
    app.run(debug=True)

app.static_folder = 'static'