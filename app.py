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

@app.route("/testdbcon")
def testdb():
    conn = mysql.connection
    cursor = conn.cursor()

    # fetchall gets all the results of query
    # fetchone gets one result from the query
    cursor.execute("select * from stocks where stockid = 4;")
    data = cursor.fetchone()
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


    return render_template("stockinfo.html", 
                            ticker=ticker,  
                            close=close,
                            openprice=openprice,
                            high=high,
                            low=low,
                            volume=volume,
                            date=date)

if __name__ == '__main__':
    app.run(debug=True)

app.static_folder = 'static'