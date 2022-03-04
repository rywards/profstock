from urllib import response
import requests
import json
from flask import Flask, render_template, request
from flask_mysqldb import MySQL
import subprocess as sp

app = Flask(__name__)
mysql = MySQL()

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'profstock'



mysql.init_app(app)


# route decorators
# these determine the location of different endpoints
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/addstock", methods=['GET','POST'])
def addstock():

    # database connection has to be done in a view
    # basically in any of the app.route decorator functions
    conn = mysql.connection
    cursor = conn.cursor()
    ticker = request.form['ticker']

    # fetchall gets all the results of query
    # fetchone gets one result from the query
    if request.method == 'GET':
        cursor.execute("select * from stocks where stockid = 4;")
        data = cursor.fetchone()
        return str(data)

    if request.method =='POST':
        cursor.execute("""INSERT INTO stocks
            (ticker,
            name)
            VALUES (%s, 'Home Depot')""", [ticker])
        cursor.execute("select * from stocks;")
        data = cursor.fetchall()
        conn.commit()
        return str(data)

@app.route("/SignUpPage.html")
def signup():
    return render_template("SignUpPage.html")

@app.route("/stocksearch.html")
def stockinfo():
    return render_template("stocksearch.html")

# Ryan Edwards
# this is where the ticker post request data goes
# we can do some calculations here as necessary
@app.route("/stockinfo.html", methods=['POST'])
def pullstockinfo():
    ticker = request.form['ticker']

    params = {
    'access_key': 'b690ef1a94c38681861a3a78272a9c98'
    }

    api_result = requests.get('http://api.marketstack.com/v1/tickers/' + ticker + '/eod/latest', params)
    api_response = api_result.json()

    close = api_response['close']
    openprice = api_response['open']
    high = api_response['high']
    low = api_response['low']
    volume = api_response['volume']
    date = api_response['date']
    symbol = api_response['symbol']


    return render_template("stockinfo.html", 
                            symbol=symbol,  
                            close=close,
                            openprice=openprice,
                            high=high,
                            low=low,
                            volume=volume,
                            date=date)

# Andrew (prototype)
# Simply gets all names from users table of the database
@app.route("/pullFromSQL", methods=['POST'])
def getFromDB():
        conn = mysql.connection
        cursor = conn.cursor()

        cursor.execute("select firstname, lastname from users;")
        data = cursor.fetchall()

        return str(data)

# Andrew (prototype)
@app.route("/postToSQL", methods=['POST'])
def writeToDB():
        conn = mysql.connection
        cursor = conn.cursor()

        firstname = request.form['firstname']
        lastname = request.form['lastname']

        cursor.execute("""INSERT INTO 
        users (
            firstname,
            lastname)
            VALUES (%s,%s)""", (firstname, lastname))

        conn.commit() 

        return render_template("AndrewPrototype.html")


# This is the actual endpoint that will add a new user's info to the db
# Still need to implement a way to check to make sure user email is not already
# in use, etc.
# Password is also just being stored as plain text right now, which is also probably
# not good
@app.route("/addNewUser", methods=['POST'])
def addToDB():
        conn = mysql.connection
        cursor = conn.cursor()

        username = request.form['username']
        email = request.form['email']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        pw = request.form['pw']

        cursor.execute("""INSERT INTO 
        users (
            username,
            email,
            firstname,
            lastname, 
            pw) 
            VALUES (%s,%s,%s,%s,%s)""", (username, email, firstname, lastname, pw))

        conn.commit() 

        return render_template("SignUpPage.html")


if __name__ == '__main__':
    app.run(debug=True)

app.static_folder = 'static'